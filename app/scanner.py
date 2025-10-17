"""
NetWatch SIEM - Network Scanner Module
Handles device discovery, ARP scanning, and network monitoring
"""

import socket
import subprocess
import platform
import re
import json
from datetime import datetime
from scapy.all import ARP, Ether, srp, conf
import psutil
from mac_vendor_lookup import MacLookup
from app import db
from app.models import Device, Event, Alert


# Disable Scapy warnings
conf.verb = 0


class NetworkScanner:
    """Main network scanner class"""
    
    def __init__(self):
        self.mac_lookup = MacLookup()
        self.mac_lookup.update_vendors()  # Update vendor database
    
    def get_local_ip(self):
        """Get the local IP address of the machine"""
        try:
            s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
            s.connect(("8.8.8.8", 80))
            local_ip = s.getsockname()[0]
            s.close()
            return local_ip
        except Exception:
            return "127.0.0.1"
    
    def get_network_range(self):
        """Calculate network range from local IP"""
        local_ip = self.get_local_ip()
        # Convert to network range (e.g., 192.168.1.0/24)
        ip_parts = local_ip.split('.')
        network_range = f"{ip_parts[0]}.{ip_parts[1]}.{ip_parts[2]}.0/24"
        return network_range
    
    def arp_scan(self, network_range=None):
        """
        Perform ARP scan to discover devices on the network
        Returns list of devices with IP and MAC addresses
        """
        if network_range is None:
            network_range = self.get_network_range()
        
        print(f"[*] Scanning network: {network_range}")
        
        try:
            # Create ARP request packet
            arp_request = ARP(pdst=network_range)
            broadcast = Ether(dst="ff:ff:ff:ff:ff:ff")
            arp_request_broadcast = broadcast / arp_request
            
            # Send packet and receive response
            answered_list = srp(arp_request_broadcast, timeout=2, verbose=False)[0]
            
            devices = []
            for element in answered_list:
                device_info = {
                    'ip': element[1].psrc,
                    'mac': element[1].hwsrc.upper(),
                    'timestamp': datetime.utcnow()
                }
                devices.append(device_info)
            
            print(f"[+] Found {len(devices)} devices")
            return devices
        
        except Exception as e:
            print(f"[!] ARP scan error: {str(e)}")
            return []
    
    def get_hostname(self, ip_address):
        """Get hostname from IP address"""
        try:
            hostname = socket.gethostbyaddr(ip_address)[0]
            return hostname
        except Exception:
            return None
    
    def get_vendor(self, mac_address):
        """Get vendor name from MAC address"""
        try:
            vendor = self.mac_lookup.lookup(mac_address)
            return vendor
        except Exception:
            return "Unknown"
    
    def ping_device(self, ip_address):
        """Ping a device to check if it's online"""
        try:
            param = '-n' if platform.system().lower() == 'windows' else '-c'
            command = ['ping', param, '1', '-w', '1000', ip_address]
            result = subprocess.run(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
            return result.returncode == 0
        except Exception:
            return False
    
    def scan_and_update_devices(self):
        """
        Main scanning function - discovers devices and updates database
        """
        print("\n" + "="*60)
        print("NetWatch SIEM - Network Scan Started")
        print("="*60)
        
        discovered_devices = self.arp_scan()
        current_time = datetime.utcnow()
        
        # Track which devices are currently online
        online_macs = set()
        
        for device_info in discovered_devices:
            ip = device_info['ip']
            mac = device_info['mac']
            online_macs.add(mac)
            
            # Check if device exists in database
            device = Device.query.filter_by(mac_address=mac).first()
            
            if device:
                # Existing device - update status
                was_offline = not device.is_online
                device.is_online = True
                device.last_seen = current_time
                
                # Check if IP changed
                if device.ip_address != ip:
                    old_ip = device.ip_address
                    device.ip_address = ip
                    
                    # Log IP change event
                    event = Event(
                        device_id=device.id,
                        event_type='ip_change',
                        severity='medium',
                        description=f'Device IP changed from {old_ip} to {ip}',
                        timestamp=current_time
                    )
                    db.session.add(event)
                    
                    # Create alert for IP change
                    alert = Alert(
                        device_id=device.id,
                        alert_type='ip_change',
                        severity='medium',
                        title='Device IP Address Changed',
                        description=f'Device {device.device_name or mac} changed IP from {old_ip} to {ip}',
                        triggered_at=current_time
                    )
                    db.session.add(alert)
                    print(f"[!] IP Change: {mac} ({old_ip} -> {ip})")
                
                # Log reconnection if device was offline
                if was_offline:
                    event = Event(
                        device_id=device.id,
                        event_type='device_reconnect',
                        severity='low',
                        description=f'Device reconnected to network',
                        timestamp=current_time
                    )
                    db.session.add(event)
                    print(f"[+] Reconnected: {ip} ({mac})")
            
            else:
                # New device discovered
                hostname = self.get_hostname(ip)
                vendor = self.get_vendor(mac)
                
                new_device = Device(
                    ip_address=ip,
                    mac_address=mac,
                    hostname=hostname,
                    vendor=vendor,
                    is_online=True,
                    is_trusted=False,
                    risk_score=50,  # Default medium risk for new devices
                    first_seen=current_time,
                    last_seen=current_time
                )
                db.session.add(new_device)
                db.session.flush()  # Get the device ID
                
                # Log new device event
                event = Event(
                    device_id=new_device.id,
                    event_type='device_join',
                    severity='medium',
                    description=f'New device detected on network',
                    details=json.dumps({
                        'ip': ip,
                        'mac': mac,
                        'vendor': vendor,
                        'hostname': hostname
                    }),
                    timestamp=current_time
                )
                db.session.add(event)
                
                # Create alert for new device
                alert = Alert(
                    device_id=new_device.id,
                    alert_type='new_device',
                    severity='high',
                    title='New Device Detected',
                    description=f'Unknown device joined network: {ip} ({vendor})',
                    triggered_at=current_time
                )
                db.session.add(alert)
                
                print(f"[!] NEW DEVICE: {ip} ({mac}) - {vendor}")
        
        # Mark devices as offline if not seen in this scan
        all_devices = Device.query.all()
        for device in all_devices:
            if device.mac_address not in online_macs and device.is_online:
                device.is_online = False
                
                # Log device disconnect
                event = Event(
                    device_id=device.id,
                    event_type='device_leave',
                    severity='low',
                    description=f'Device disconnected from network',
                    timestamp=current_time
                )
                db.session.add(event)
                print(f"[-] Offline: {device.ip_address} ({device.mac_address})")
        
        # Commit all changes
        db.session.commit()
        
        print("="*60)
        print(f"Scan Complete - {len(discovered_devices)} devices online")
        print("="*60 + "\n")
        
        return {
            'total_devices': len(all_devices),
            'online_devices': len(discovered_devices),
            'new_devices': len([d for d in discovered_devices if d['mac'] not in [dev.mac_address for dev in all_devices]])
        }


class TrafficMonitor:
    """Monitor network traffic (Pro feature)"""
    
    @staticmethod
    def get_network_stats():
        """Get current network statistics"""
        try:
            net_io = psutil.net_io_counters()
            return {
                'bytes_sent': net_io.bytes_sent,
                'bytes_recv': net_io.bytes_recv,
                'packets_sent': net_io.packets_sent,
                'packets_recv': net_io.packets_recv
            }
        except Exception as e:
            print(f"[!] Traffic monitor error: {str(e)}")
            return None
    
    @staticmethod
    def get_connections():
        """Get active network connections"""
        try:
            connections = psutil.net_connections(kind='inet')
            return connections
        except Exception as e:
            print(f"[!] Connection monitor error: {str(e)}")
            return []


class RuleEngine:
    """Process rules and trigger alerts"""
    
    @staticmethod
    def check_reconnect_frequency(device_id, threshold=5, time_window=3600):
        """Check if device reconnects too frequently"""
        from datetime import timedelta
        
        device = Device.query.get(device_id)
        if not device:
            return False
        
        # Count reconnect events in the last hour
        time_ago = datetime.utcnow() - timedelta(seconds=time_window)
        reconnect_count = Event.query.filter(
            Event.device_id == device_id,
            Event.event_type == 'device_reconnect',
            Event.timestamp >= time_ago
        ).count()
        
        if reconnect_count >= threshold:
            # Create alert
            alert = Alert(
                device_id=device_id,
                alert_type='frequent_reconnect',
                severity='high',
                title='Frequent Reconnection Detected',
                description=f'Device reconnected {reconnect_count} times in the last hour',
                triggered_at=datetime.utcnow()
            )
            db.session.add(alert)
            db.session.commit()
            return True
        
        return False
    
    @staticmethod
    def check_inactive_devices(threshold_hours=24):
        """Check for devices inactive for long period"""
        from datetime import timedelta
        
        time_ago = datetime.utcnow() - timedelta(hours=threshold_hours)
        inactive_devices = Device.query.filter(
            Device.last_seen < time_ago,
            Device.is_online == False
        ).all()
        
        for device in inactive_devices:
            # Check if alert already exists
            existing_alert = Alert.query.filter(
                Alert.device_id == device.id,
                Alert.alert_type == 'device_inactive',
                Alert.status == 'active'
            ).first()
            
            if not existing_alert:
                alert = Alert(
                    device_id=device.id,
                    alert_type='device_inactive',
                    severity='low',
                    title='Device Inactive',
                    description=f'Device has been offline for more than {threshold_hours} hours',
                    triggered_at=datetime.utcnow()
                )
                db.session.add(alert)
        
        db.session.commit()
        return len(inactive_devices)