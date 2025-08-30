#!/bin/bash
# Balanced Process Priority Management for Kali Linux
# Created: 2023-07-18

# Configuration - Set your preferred nice values here
CRITICAL_UI="-15"      # Window managers, display servers
IMPORTANT_APPS="-10"   # Main applications you use frequently
SYSTEM_SERVICES="-5"   # Important background services
NORMAL="0"             # Default for general processes
LOW="10"               # Non-essential background tasks

# Colors for output
GREEN="\033[0;32m"
YELLOW="\033[0;33m"
BLUE="\033[0;34m"
RED="\033[0;31m"
NC="\033[0m" # No Color

# Must be run as root
if [ "$EUID" -ne 0 ]; then
  echo -e "${RED}Please run as root or with sudo${NC}"
  exit 1
fi

echo -e "${GREEN}===== Balanced Priority Manager =====${NC}"
echo -e "${YELLOW}Setting tiered priorities for better system performance${NC}"
echo ""

# Function to set process priority by pattern and level
set_priority() {
    local pattern="$1"
    local nice_level="$2"
    local category="$3"
    
    echo -e "${BLUE}Setting $category priority ($nice_level) for: $pattern${NC}"
    
    # Find PIDs matching pattern and adjust priority
    pids=$(pgrep -f "$pattern")
    if [ -n "$pids" ]; then
        for pid in $pids; do
            # Skip the current script
            if [ "$pid" -ne "$$" ]; then
                current_nice=$(ps -o ni -p $pid | tail -1 | tr -d ' ')
                process_name=$(ps -p $pid -o comm= | head -1)
                echo "  · $process_name (PID: $pid) from $current_nice to $nice_level"
                renice $nice_level -p $pid >/dev/null 2>&1
            fi
        done
    else
        echo "  · No matching processes found"
    fi
}

# Function to adjust priorities dynamically for the focused window
focus_priority() {
    echo -e "${GREEN}Starting dynamic focus priority...${NC}"
    echo "Press Ctrl+C to stop"
    
    while true; do
        # Get the focused window's PID using xdotool (need to install it)
        focused_pid=$(xdotool getwindowfocus getwindowpid 2>/dev/null)
        if [ -n "$focused_pid" ]; then
            focused_name=$(ps -p $focused_pid -o comm= | head -1)
            renice -10 -p $focused_pid >/dev/null 2>&1
            echo -ne "\rGiving high priority to focused application: $focused_name (PID: $focused_pid)       "
            
            # Also prioritize child processes
            child_pids=$(pgrep -P $focused_pid)
            for child in $child_pids; do
                renice -10 -p $child >/dev/null 2>&1
            done
        fi
        sleep 2
    done
}

# Function to reset all priorities
reset_priorities() {
    echo -e "${YELLOW}Resetting all process priorities to normal...${NC}"
    
    # Get all PIDs except kernel processes
    pids=$(ps -eo pid --no-headers | grep -v "^1$")
    
    for pid in $pids; do
        # Skip the current script
        if [ "$pid" -ne "$$" ]; then
            current_nice=$(ps -o ni -p $pid 2>/dev/null | tail -1 | tr -d ' ')
            if [[ "$current_nice" != "$NORMAL" && "$current_nice" != "" ]]; then
                process_name=$(ps -p $pid -o comm= 2>/dev/null | head -1)
                if [ -n "$process_name" ]; then
                    echo "  · Resetting $process_name (PID: $pid) from $current_nice to $NORMAL"
                    renice $NORMAL -p $pid >/dev/null 2>&1
                fi
            fi
        fi
    done
    echo "Done resetting priorities."
}

# Function to show current priority stats
show_stats() {
    echo -e "${GREEN}===== Current Priority Statistics =====${NC}"
    
    echo -e "${BLUE}Priority counts:${NC}"
    ps -eo ni --no-headers | sort | uniq -c | sort -n
    
    echo -e "\n${BLUE}Top 10 highest priority processes:${NC}"
    ps -eo pid,ni,comm --no-headers | sort -n -k2 | head -10
    
    echo -e "\n${BLUE}Top 10 lowest priority processes:${NC}"
    ps -eo pid,ni,comm --no-headers | sort -n -k2 -r | head -10
}

# Main functionality based on command argument
case "$1" in
    "apply")
        echo -e "${GREEN}Applying balanced priority scheme...${NC}"
        
        # Critical UI processes (highest priority)
        set_priority "Xorg|xorg|wayland|weston" "$CRITICAL_UI" "CRITICAL UI"
        set_priority "xfwm4|kwin|mutter|compiz" "$CRITICAL_UI" "CRITICAL UI"
        set_priority "lightdm" "$CRITICAL_UI" "CRITICAL UI"
        
        # Important applications
        set_priority "firefox|chromium|browser" "$IMPORTANT_APPS" "IMPORTANT APPS"
        set_priority "terminal|konsole|xfce4-terminal" "$IMPORTANT_APPS" "IMPORTANT APPS"
        set_priority "metasploit|msfconsole|burpsuite|wireshark" "$IMPORTANT_APPS" "IMPORTANT APPS"
        
        # System services
        set_priority "systemd (?!-user)" "$SYSTEM_SERVICES" "SYSTEM SERVICES"
        set_priority "NetworkManager|wpa_supplicant" "$SYSTEM_SERVICES" "SYSTEM SERVICES"
        set_priority "dbus-daemon" "$SYSTEM_SERVICES" "SYSTEM SERVICES"
        
        # Lower priority for non-essential services
        set_priority "tracker|zeitgeist|indexing" "$LOW" "LOW PRIORITY"
        set_priority "cups|printer|bluetooth" "$LOW" "LOW PRIORITY"
        
        echo -e "${GREEN}Balanced priority scheme applied successfully!${NC}"
        ;;
        
    "focus")
        # Check if xdotool is installed
        if ! command -v xdotool &> /dev/null; then
            echo -e "${RED}xdotool is required but not installed.${NC}"
            echo "Install it with: sudo apt install xdotool"
            exit 1
        fi
        focus_priority
        ;;
        
    "reset")
        reset_priorities
        ;;
        
    "stats")
        show_stats
        ;;
        
    *)
        echo -e "${GREEN}===== Balanced Priority Manager Usage =====${NC}"
        echo -e "sudo $0 ${YELLOW}apply${NC}  - Apply balanced priority scheme"
        echo -e "sudo $0 ${YELLOW}focus${NC}  - Dynamically prioritize focused window"
        echo -e "sudo $0 ${YELLOW}reset${NC}  - Reset all priorities to normal"
        echo -e "sudo $0 ${YELLOW}stats${NC}  - Show current priority statistics"
        echo ""
        echo -e "${BLUE}Priority Levels:${NC}"
        echo "  Critical UI:       $CRITICAL_UI (display, window managers)"
        echo "  Important Apps:    $IMPORTANT_APPS (browsers, terminals, security tools)"
        echo "  System Services:   $SYSTEM_SERVICES (system daemons, networking)"
        echo "  Normal:            $NORMAL (default for most processes)"
        echo "  Low Priority:      $LOW (non-essential background tasks)"
        ;;
esac
