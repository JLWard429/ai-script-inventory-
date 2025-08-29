#!/bin/bash
# Kali Linux Performance Optimization Script

echo "Starting Kali Linux performance optimization..."

# CPU optimization
echo "Setting CPU governor to performance mode..."
echo performance | sudo tee /sys/devices/system/cpu/cpu*/cpufreq/scaling_governor

# Memory optimization
echo "Optimizing memory settings..."
echo 10 | sudo tee /proc/sys/vm/swappiness
echo "vm.swappiness=10" | sudo tee -a /etc/sysctl.conf
echo 50 | sudo tee /proc/sys/vm/vfs_cache_pressure
echo "vm.vfs_cache_pressure=50" | sudo tee -a /etc/sysctl.conf

# Filesystem optimization
echo "Optimizing filesystem settings..."
echo "fs.inotify.max_user_watches=524288" | sudo tee -a /etc/sysctl.conf

# Apply sysctl changes
sudo sysctl -p

# I/O scheduling optimization
echo "Optimizing I/O scheduling..."
if [ -e /sys/block/sda/queue/scheduler ]; then
  echo deadline | sudo tee /sys/block/sda/queue/scheduler
fi

# Disable unnecessary services
echo "Disabling unnecessary services..."
for service in bluetooth cups avahi-daemon ModemManager; do
  sudo systemctl stop $service 2>/dev/null
  sudo systemctl disable $service 2>/dev/null
  echo "  - Disabled $service"
done

echo "Optimization complete! Consider rebooting your system."
