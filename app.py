#!/usr/bin/env python3
"""
🧠 OVERTHINKING METER - Track & Analyze Your Mental Patterns
A mental wellness tool to identify overthinking patterns and reduce anxiety
"""

import sys
import os
from datetime import datetime
from collections import defaultdict, Counter

# Colorama for cross-platform colored output
try:
    from colorama import init, Fore, Style
    init(autoreset=True)
    HAS_COLOR = True
except ImportError:
    HAS_COLOR = False
    class Fore:
        GREEN = RED = YELLOW = CYAN = MAGENTA = BLUE = ""
    class Style:
        BRIGHT = RESET_ALL = ""

# Configuration
THOUGHTS_FILE = "overthinking_log.txt"
DAILY_DATA_FILE = "daily_overthinking.csv"
REPORT_FILE = "overthinking_report.txt"

# Categories for overthinking
CATEGORIES = {
    '1': '💼 Career/Work',
    '2': '❤️ Relationships',
    '3': '🔮 Future/Uncertainty',
    '4': '💰 Money/Finance',
    '5': '🏥 Health/Body',
    '6': '👥 Social/Friends',
    '7': '🎯 Other'
}

def print_success(msg):
    """Print success message in green"""
    print(f"{Fore.GREEN}✓ {msg}{Style.RESET_ALL}")

def print_error(msg):
    """Print error message in red"""
    print(f"{Fore.RED}✗ {msg}{Style.RESET_ALL}")

def print_info(msg):
    """Print info message in cyan"""
    print(f"{Fore.CYAN}ℹ {msg}{Style.RESET_ALL}")

def print_warning(msg):
    """Print warning message in yellow"""
    print(f"{Fore.YELLOW}⚠ {msg}{Style.RESET_ALL}")

def print_header(msg):
    """Print header in bright magenta"""
    print(f"\n{Fore.MAGENTA}{Style.BRIGHT}{'='*60}")
    print(f"{msg:^60}")
    print(f"{'='*60}{Style.RESET_ALL}")

def get_time_period(hour):
    """Get time period label"""
    if 5 <= hour < 12:
        return "🌅 Morning"
    elif 12 <= hour < 17:
        return "☀️ Afternoon"
    elif 17 <= hour < 21:
        return "🌆 Evening"
    else:
        return "🌙 Night"

class OverthinkingTracker:
    def __init__(self, dry_run=False):
        self.thoughts = []
        self.dry_run = dry_run
        self.load_thoughts()
        
        if dry_run:
            print_warning("DRY RUN MODE: No changes will be saved")
    
    def load_thoughts(self):
        """Load overthinking logs from file"""
        if not os.path.exists(THOUGHTS_FILE):
            return
        
        try:
            with open(THOUGHTS_FILE, 'r', encoding='utf-8') as f:
                for line in f:
                    line = line.strip()
                    if line and '|' in line:
                        parts = line.split('|')
                        if len(parts) >= 4:
                            thought = {
                                'timestamp': parts[0].strip(),
                                'category': parts[1].strip(),
                                'intensity': int(parts[2].strip()) if parts[2].strip().isdigit() else 5,
                                'note': parts[3].strip() if len(parts) > 3 else ''
                            }
                            self.thoughts.append(thought)
            print_success(f"Loaded {len(self.thoughts)} overthinking entries")
        except Exception as e:
            print_error(f"Error loading data: {e}")
    
    def save_thoughts(self):
        """Save overthinking logs to file"""
        if self.dry_run:
            print_info("[DRY RUN] Would save overthinking log")
            return
        
        try:
            with open(THOUGHTS_FILE, 'w', encoding='utf-8') as f:
                for thought in self.thoughts:
                    f.write(f"{thought['timestamp']}|{thought['category']}|{thought['intensity']}|{thought['note']}\n")
            print_success(f"Saved {len(self.thoughts)} entries to {THOUGHTS_FILE}")
        except Exception as e:
            print_error(f"Error saving data: {e}")
    
    def log_overthinking(self):
        """Log a new overthinking episode"""
        print_header("📝 LOG OVERTHINKING EPISODE")
        
        print(f"{Fore.YELLOW}Koi baat nahi, happens to everyone! Let's log it:{Style.RESET_ALL}\n")
        
        try:
            # Show categories
            print(f"{Fore.CYAN}Select overthinking category:{Style.RESET_ALL}")
            for key, category in CATEGORIES.items():
                print(f"  {key}. {category}")
            
            cat_choice = input(f"\n{Fore.YELLOW}Enter category (1-7) or 'cancel': {Style.RESET_ALL}").strip()
            
            if cat_choice.lower() == 'cancel':
                print_info("Cancelled")
                return
            
            if cat_choice not in CATEGORIES:
                print_error("Invalid category")
                return
            
            # Get intensity
            print(f"\n{Fore.CYAN}Intensity level:{Style.RESET_ALL}")
            print("  1-3  : 😌 Mild (just thinking)")
            print("  4-6  : 😰 Moderate (can't focus)")
            print("  7-10 : 😱 Severe (can't sleep/function)")
            
            intensity_str = input(f"\n{Fore.YELLOW}Rate intensity (1-10): {Style.RESET_ALL}").strip()
            
            try:
                intensity = int(intensity_str)
                if not 1 <= intensity <= 10:
                    print_error("Please enter 1-10")
                    return
            except ValueError:
                print_error("Please enter a valid number")
                return
            
            # Optional note
            note = input(f"\n{Fore.YELLOW}Quick note (optional, or press Enter): {Style.RESET_ALL}").strip()
            
            # Create entry
            thought = {
                'timestamp': datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                'category': CATEGORIES[cat_choice],
                'intensity': intensity,
                'note': note
            }
            
            self.thoughts.append(thought)
            self.save_thoughts()
            
            # Encouraging message based on intensity
            if intensity <= 3:
                print_success("Logged! Light thoughts are normal - you got this! 💪")
            elif intensity <= 6:
                print_success("Logged! Remember to breathe deeply 🌬️")
            else:
                print_success("Logged! Consider talking to someone you trust 🤗")
                print_info("High intensity detected. Self-care reminder: Take a break!")
            
        except KeyboardInterrupt:
            print_info("\nCancelled")
        except Exception as e:
            print_error(f"Unexpected error: {e}")
    
    def view_history(self):
        """View recent overthinking history"""
        print_header("📜 YOUR OVERTHINKING HISTORY")
        
        if not self.thoughts:
            print_info("No entries yet. Start logging to see patterns!")
            return
        
        # Show last 10 entries
        recent = self.thoughts[-10:]
        
        print(f"{Fore.CYAN}Showing last {len(recent)} entries:{Style.RESET_ALL}\n")
        
        for i, thought in enumerate(reversed(recent), 1):
            intensity_bar = "█" * thought['intensity']
            color = Fore.GREEN if thought['intensity'] <= 3 else Fore.YELLOW if thought['intensity'] <= 6 else Fore.RED
            
            print(f"{i}. {Fore.CYAN}{thought['timestamp']}{Style.RESET_ALL}")
            print(f"   {thought['category']}")
            print(f"   Intensity: {color}{intensity_bar}{Style.RESET_ALL} ({thought['intensity']}/10)")
            if thought['note']:
                print(f"   Note: {thought['note']}")
            print()
        
        print(f"{Fore.MAGENTA}{'─'*60}{Style.RESET_ALL}")
        print(f"Total entries: {len(self.thoughts)}")
    
    def analyze_patterns(self):
        """Analyze overthinking patterns"""
        print_header("🔍 PATTERN ANALYSIS")
        
        if not self.thoughts:
            print_warning("Not enough data yet. Keep logging!")
            return
        
        # Time analysis
        hour_counts = defaultdict(int)
        period_counts = defaultdict(int)
        category_counts = Counter()
        intensity_sum = 0
        
        for thought in self.thoughts:
            try:
                dt = datetime.strptime(thought['timestamp'], "%Y-%m-%d %H:%M:%S")
                hour = dt.hour
                hour_counts[hour] += 1
                period_counts[get_time_period(hour)] += 1
                category_counts[thought['category']] += 1
                intensity_sum += thought['intensity']
            except:
                continue
        
        if not hour_counts:
            print_error("Could not analyze timestamps")
            return
        
        # Find peak hour
        peak_hour = max(hour_counts, key=hour_counts.get)
        peak_hour_12 = peak_hour if peak_hour <= 12 else peak_hour - 12
        am_pm = "AM" if peak_hour < 12 else "PM"
        
        # Find peak period
        peak_period = max(period_counts, key=period_counts.get)
        
        # Find top category
        top_category = category_counts.most_common(1)[0] if category_counts else ("Unknown", 0)
        
        # Average intensity
        avg_intensity = intensity_sum / len(self.thoughts)
        
        # Display insights
        print(f"\n{Fore.CYAN}{'='*60}{Style.RESET_ALL}")
        print(f"{Fore.YELLOW}{Style.BRIGHT}🌟 YOUR OVERTHINKING INSIGHTS 🌟{Style.RESET_ALL}\n")
        
        print(f"{Fore.GREEN}Total Episodes:{Style.RESET_ALL}       {len(self.thoughts)}")
        print(f"{Fore.GREEN}Average Intensity:{Style.RESET_ALL}   {avg_intensity:.1f}/10")
        
        intensity_emoji = "😌" if avg_intensity <= 3 else "😰" if avg_intensity <= 6 else "😱"
        print(f"                        {intensity_emoji}\n")
        
        print(f"{Fore.MAGENTA}{Style.BRIGHT}⏰ TIME PATTERNS:{Style.RESET_ALL}")
        print(f"  Peak Hour:     {peak_hour_12}:00 {am_pm} 🕐")
        print(f"  Peak Period:   {peak_period}")
        print(f"  {Fore.YELLOW}→ You overthink most during {peak_period.split()[1]}!{Style.RESET_ALL}\n")
        
        print(f"{Fore.MAGENTA}{Style.BRIGHT}📊 CATEGORY BREAKDOWN:{Style.RESET_ALL}")
        print(f"  Top Concern:   {top_category[0]} ({top_category[1]} times)")
        
        # Show top 3 categories
        for i, (cat, count) in enumerate(category_counts.most_common(3), 1):
            percentage = (count / len(self.thoughts)) * 100
            bar_length = int(percentage / 3)
            bar = "█" * bar_length
            print(f"  {i}. {cat}: {Fore.CYAN}{bar}{Style.RESET_ALL} {percentage:.0f}%")
        
        print(f"\n{Fore.CYAN}{'='*60}{Style.RESET_ALL}")
        
        # Recommendations
        print(f"\n{Fore.GREEN}{Style.BRIGHT}💡 PERSONALIZED TIPS:{Style.RESET_ALL}")
        
        if peak_hour >= 22 or peak_hour <= 4:
            print(f"  • {Fore.YELLOW}Late night overthinking detected!{Style.RESET_ALL}")
            print(f"    Try: Set phone down at 10 PM, journal before bed 📓")
        
        if avg_intensity >= 7:
            print(f"  • {Fore.RED}High intensity levels!{Style.RESET_ALL}")
            print(f"    Consider: Talking to a counselor or trusted friend 🤝")
        
        if top_category[0].startswith("🔮"):
            print(f"  • {Fore.YELLOW}Future anxiety common!{Style.RESET_ALL}")
            print(f"    Practice: Focus on present moment, 5-4-3-2-1 grounding 🧘")
        
        if len(self.thoughts) > 10:
            recent_week = self.thoughts[-7:]
            if len(recent_week) >= 5:
                print(f"  • {Fore.YELLOW}Frequent overthinking lately!{Style.RESET_ALL}")
                print(f"    Self-care reminder: Take breaks, exercise, hydrate 💧")
        
        print(f"\n{Fore.GREEN}Remember: Overthinking is normal, but you can manage it! 🌟{Style.RESET_ALL}")
        
        # Draw time distribution chart
        self._draw_time_chart(hour_counts)
    
    def weekly_summary(self):
        """Generate comprehensive weekly summary"""
        print_header("📊 WEEKLY SUMMARY REPORT")
        
        if not self.thoughts:
            print_warning("Not enough data for weekly summary")
            return
        
        # Get data from last 7 days
        from datetime import timedelta
        now = datetime.now()
        seven_days_ago = now - timedelta(days=7)
        
        weekly_thoughts = []
        for thought in self.thoughts:
            try:
                dt = datetime.strptime(thought['timestamp'], "%Y-%m-%d %H:%M:%S")
                if dt >= seven_days_ago:
                    weekly_thoughts.append(thought)
            except:
                continue
        
        if not weekly_thoughts:
            print_warning("No entries in the last 7 days")
            print_info("Start logging to see your weekly summary!")
            return
        
        # Calculate statistics
        total_episodes = len(weekly_thoughts)
        avg_intensity = sum(t['intensity'] for t in weekly_thoughts) / total_episodes
        
        # Day-wise breakdown
        day_counts = defaultdict(int)
        for thought in weekly_thoughts:
            try:
                dt = datetime.strptime(thought['timestamp'], "%Y-%m-%d %H:%M:%S")
                day_name = dt.strftime("%A")
                day_counts[day_name] += 1
            except:
                continue
        
        # Category breakdown
        category_counts = Counter(t['category'] for t in weekly_thoughts)
        
        # High intensity count
        high_intensity = sum(1 for t in weekly_thoughts if t['intensity'] >= 7)
        
        # Display summary
        print(f"\n{Fore.CYAN}{'='*60}{Style.RESET_ALL}")
        print(f"{Fore.YELLOW}{Style.BRIGHT}📅 LAST 7 DAYS OVERVIEW{Style.RESET_ALL}\n")
        
        print(f"{Fore.GREEN}Total Episodes:{Style.RESET_ALL}      {total_episodes}")
        print(f"{Fore.GREEN}Daily Average:{Style.RESET_ALL}       {total_episodes/7:.1f} episodes/day")
        print(f"{Fore.GREEN}Avg Intensity:{Style.RESET_ALL}       {avg_intensity:.1f}/10")
        
        intensity_status = "😌 Manageable" if avg_intensity <= 4 else "😰 Moderate" if avg_intensity <= 7 else "😱 High"
        print(f"                        {intensity_status}\n")
        
        if high_intensity > 0:
            print(f"{Fore.RED}⚠ High Intensity Episodes: {high_intensity}{Style.RESET_ALL}")
            print(f"  {Fore.YELLOW}Consider reaching out for support!{Style.RESET_ALL}\n")
        
        # Most active day
        if day_counts:
            worst_day = max(day_counts, key=day_counts.get)
            best_day = min(day_counts, key=day_counts.get) if len(day_counts) > 1 else None
            
            print(f"{Fore.MAGENTA}{Style.BRIGHT}📅 DAY ANALYSIS:{Style.RESET_ALL}")
            print(f"  Most Episodes:  {Fore.RED}{worst_day} ({day_counts[worst_day]} times){Style.RESET_ALL}")
            if best_day and best_day != worst_day:
                print(f"  Least Episodes: {Fore.GREEN}{best_day} ({day_counts[best_day]} times){Style.RESET_ALL}")
        
        # Top concerns
        print(f"\n{Fore.MAGENTA}{Style.BRIGHT}🎯 TOP CONCERNS THIS WEEK:{Style.RESET_ALL}")
        for i, (cat, count) in enumerate(category_counts.most_common(3), 1):
            percentage = (count / total_episodes) * 100
            print(f"  {i}. {cat} - {count} times ({percentage:.0f}%)")
        
        # Weekly trend
        print(f"\n{Fore.MAGENTA}{Style.BRIGHT}📈 WEEKLY TREND:{Style.RESET_ALL}")
        
        if len(weekly_thoughts) >= 6:
            first_half = weekly_thoughts[:len(weekly_thoughts)//2]
            second_half = weekly_thoughts[len(weekly_thoughts)//2:]
            
            first_avg = sum(t['intensity'] for t in first_half) / len(first_half)
            second_avg = sum(t['intensity'] for t in second_half) / len(second_half)
            
            if second_avg < first_avg * 0.85:
                trend = "📉 IMPROVING!"
                color = Fore.GREEN
                message = "Great progress! Keep up the good work! 🎉"
            elif second_avg > first_avg * 1.15:
                trend = "📈 INCREASING"
                color = Fore.RED
                message = "Stress building up. Time for self-care! 🛀"
            else:
                trend = "➡️ STABLE"
                color = Fore.YELLOW
                message = "Staying consistent. Keep monitoring! 👀"
            
            print(f"  {color}{Style.BRIGHT}{trend}{Style.RESET_ALL}")
            print(f"  {message}")
        
        # Personalized recommendations
        print(f"\n{Fore.GREEN}{Style.BRIGHT}💡 THIS WEEK'S RECOMMENDATIONS:{Style.RESET_ALL}")
        
        if total_episodes >= 10:
            print(f"  • {Fore.YELLOW}High frequency detected!{Style.RESET_ALL}")
            print(f"    Try: Schedule worry time (15 min daily) to contain overthinking")
        
        if avg_intensity >= 6:
            print(f"  • {Fore.YELLOW}Intensity is high!{Style.RESET_ALL}")
            print(f"    Practice: Progressive muscle relaxation before bed")
        
        if category_counts:
            top_category = category_counts.most_common(1)[0][0]
            if "Career" in top_category:
                print(f"  • Work stress dominating your thoughts")
                print(f"    Tip: Set clear work-life boundaries, take regular breaks")
            elif "Future" in top_category:
                print(f"  • Future anxiety is high")
                print(f"    Tip: Focus on what you CAN control today")
            elif "Relationships" in top_category:
                print(f"  • Relationship concerns present")
                print(f"    Tip: Consider having open conversations with loved ones")
        
        # Visual weekly chart
        self._draw_weekly_chart(day_counts)
        
        print(f"\n{Fore.CYAN}{'='*60}{Style.RESET_ALL}")
        print(f"{Fore.GREEN}Remember: Progress isn't linear. Be patient with yourself! 💚{Style.RESET_ALL}")

    def _draw_weekly_chart(self, day_counts):
        """Draw weekly bar chart"""
        print(f"\n{Fore.MAGENTA}{Style.BRIGHT}📊 EPISODES BY DAY:{Style.RESET_ALL}\n")
        
        if not day_counts:
            return
        
        days_order = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']
        max_count = max(day_counts.values()) if day_counts else 1
        
        for day in days_order:
            count = day_counts.get(day, 0)
            if count > 0:
                bar_length = int((count / max_count) * 30)
                bar = "█" * bar_length
                if count >= max_count * 0.8:
                    color = Fore.RED
                elif count >= max_count * 0.5:
                    color = Fore.YELLOW
                else:
                    color = Fore.GREEN
                print(f"{day[:3]:>3} | {color}{bar}{Style.RESET_ALL} {count}")

    def _draw_time_chart(self, hour_counts):
        """Draw ASCII chart of overthinking by hour"""
        print_header("📊 HOURLY DISTRIBUTION")
        
        if not hour_counts:
            return
        
        periods = {
            "00-03": sum(hour_counts.get(h, 0) for h in range(0, 4)),
            "04-07": sum(hour_counts.get(h, 0) for h in range(4, 8)),
            "08-11": sum(hour_counts.get(h, 0) for h in range(8, 12)),
            "12-15": sum(hour_counts.get(h, 0) for h in range(12, 16)),
            "16-19": sum(hour_counts.get(h, 0) for h in range(16, 20)),
            "20-23": sum(hour_counts.get(h, 0) for h in range(20, 24)),
        }
        
        max_period = max(periods.values()) if periods else 1
        
        for period, count in periods.items():
            bar_length = int((count / max_period) * 40) if max_period > 0 else 0
            bar = "█" * bar_length
            
            if count == max_period:
                color = Fore.RED
            elif count >= max_period * 0.6:
                color = Fore.YELLOW
            else:
                color = Fore.GREEN
            
            print(f"{period} hrs | {color}{bar}{Style.RESET_ALL} ({count})")


class DailyDataAnalyzer:
    @staticmethod
    def read_daily_data(filename):
        """Read daily overthinking minutes from CSV"""
        data = []
        
        if not os.path.exists(filename):
            print_error(f"File '{filename}' not found")
            print_info("Create 'daily_overthinking.csv' with format: Date,Minutes")
            return data
        
        try:
            with open(filename, 'r') as f:
                lines = f.readlines()
            
            for line_num, line in enumerate(lines, 1):
                line = line.strip()
                
                # Skip empty lines
                if not line:
                    continue
                
                # Skip header
                if line_num == 1 or any(keyword in line.lower() for keyword in ['date', 'minutes', 'time', 'duration']):
                    print_info(f"Skipping header: {line}")
                    continue
                
                # Parse data
                parts = line.split(',')
                if len(parts) >= 2:
                    try:
                        date_str = parts[0].strip()
                        minutes = float(parts[1].strip())
                        data.append({'date': date_str, 'minutes': minutes})
                    except ValueError:
                        print_warning(f"Skipping invalid line {line_num}: {line}")
                        continue
            
            print_success(f"Successfully read {len(data)} daily entries from {filename}")
            return data
            
        except Exception as e:
            print_error(f"Error reading file: {e}")
            return data
    
    @staticmethod
    def calculate_stats(data):
        """Calculate comprehensive statistics"""
        if not data:
            return None
        
        minutes = [d['minutes'] for d in data]
        
        stats = {
            'days_tracked': len(minutes),
            'avg_minutes': sum(minutes) / len(minutes),
            'median_minutes': DailyDataAnalyzer._calculate_median(minutes),
            'highest_day': max(minutes),
            'lowest_day': min(minutes),
            'total_hours': sum(minutes) / 60,
            'trend': DailyDataAnalyzer._calculate_trend(minutes)
        }
        return stats
    
    @staticmethod
    def _calculate_median(values):
        """Calculate median value"""
        sorted_vals = sorted(values)
        n = len(sorted_vals)
        mid = n // 2
        
        if n % 2 == 0:
            return (sorted_vals[mid - 1] + sorted_vals[mid]) / 2
        else:
            return sorted_vals[mid]
    
    @staticmethod
    def _calculate_trend(minutes):
        """Simple trend calculation (improving/worsening)"""
        if len(minutes) < 2:
            return "neutral"
        
        # Compare first half vs second half
        mid = len(minutes) // 2
        first_half_avg = sum(minutes[:mid]) / mid if mid > 0 else 0
        second_half_avg = sum(minutes[mid:]) / (len(minutes) - mid) if len(minutes) > mid else 0
        
        if second_half_avg < first_half_avg * 0.9:
            return "improving"
        elif second_half_avg > first_half_avg * 1.1:
            return "increasing"
        else:
            return "stable"
    
    @staticmethod
    def analyze_daily_data():
        """Main CSV analysis function"""
        print_header("📈 DAILY OVERTHINKING TIME ANALYSIS")
        
        data = DailyDataAnalyzer.read_daily_data(DAILY_DATA_FILE)
        
        if not data:
            print_warning("No daily data found to analyze")
            print_info("\nCreate a CSV file with format:")
            print("Date,Minutes")
            print("2025-01-15,45")
            print("2025-01-16,30")
            return
        
        stats = DailyDataAnalyzer.calculate_stats(data)
        
        # Display statistics
        print(f"\n{Fore.CYAN}{'─'*60}{Style.RESET_ALL}")
        print(f"{Fore.GREEN}Days Tracked:{Style.RESET_ALL}        {stats['days_tracked']}")
        print(f"{Fore.GREEN}Avg Minutes/Day:{Style.RESET_ALL}    {stats['avg_minutes']:.2f} minutes")
        print(f"{Fore.GREEN}Median Minutes:{Style.RESET_ALL}      {stats['median_minutes']:.2f} minutes")
        print(f"{Fore.GREEN}Highest Day:{Style.RESET_ALL}         {stats['highest_day']:.2f} minutes")
        print(f"{Fore.GREEN}Lowest Day:{Style.RESET_ALL}          {stats['lowest_day']:.2f} minutes")
        print(f"{Fore.GREEN}Total Time:{Style.RESET_ALL}          {stats['total_hours']:.1f} hours")
        
        # Trend analysis
        trend_emoji = "📉" if stats['trend'] == "improving" else "📈" if stats['trend'] == "increasing" else "➡️"
        trend_color = Fore.GREEN if stats['trend'] == "improving" else Fore.RED if stats['trend'] == "increasing" else Fore.YELLOW
        print(f"\n{trend_color}{Style.BRIGHT}Trend: {stats['trend'].upper()} {trend_emoji}{Style.RESET_ALL}")
        
        if stats['trend'] == "improving":
            print(f"{Fore.GREEN}Great job! Your overthinking is decreasing! 🎉{Style.RESET_ALL}")
        elif stats['trend'] == "increasing":
            print(f"{Fore.YELLOW}Heads up: Consider stress management techniques 🧘{Style.RESET_ALL}")
        
        print(f"{Fore.CYAN}{'─'*60}{Style.RESET_ALL}\n")
        
        # Draw chart
        DailyDataAnalyzer.draw_trend_chart(data)
        
        return stats
    
    @staticmethod
    def draw_trend_chart(data):
        """Draw ASCII trend chart"""
        print_header("📊 DAILY TREND CHART")
        
        if len(data) < 2:
            print_info("Need more data points for trend chart")
            return
        
        minutes = [d['minutes'] for d in data]
        max_val = max(minutes)
        min_val = min(minutes)
        
        # Show last 14 days or all if less
        recent_data = data[-14:]
        
        print(f"{Fore.CYAN}Last {len(recent_data)} days:{Style.RESET_ALL}\n")
        
        for i, entry in enumerate(recent_data):
            date = entry['date'][-5:]  # Last 5 chars (MM-DD)
            mins = entry['minutes']
            
            # Normalize to 40 chars
            if max_val > min_val:
                bar_length = int(((mins - min_val) / (max_val - min_val)) * 40)
            else:
                bar_length = 20
            
            bar = "█" * bar_length
            
            # Color by intensity
            if mins > 60:
                color = Fore.RED
            elif mins > 30:
                color = Fore.YELLOW
            else:
                color = Fore.GREEN
            
            print(f"{date} | {color}{bar}{Style.RESET_ALL} {mins:.0f}m")
    
    @staticmethod
    def export_report(stats, data):
        """Export detailed report"""
        if not stats:
            print_error("No statistics to export")
            return
        
        try:
            with open(REPORT_FILE, 'w') as f:
                f.write("="*60 + "\n")
                f.write("OVERTHINKING PATTERN ANALYSIS REPORT\n")
                f.write(f"Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
                f.write("="*60 + "\n\n")
                
                f.write("DAILY STATISTICS\n")
                f.write("-"*60 + "\n")
                f.write(f"Days Tracked:        {stats['days_tracked']}\n")
                f.write(f"Avg Minutes/Day:     {stats['avg_minutes']:.2f}\n")
                f.write(f"Median Minutes:      {stats['median_minutes']:.2f}\n")
                f.write(f"Highest Day:         {stats['highest_day']:.2f} minutes\n")
                f.write(f"Lowest Day:          {stats['lowest_day']:.2f} minutes\n")
                f.write(f"Total Time:          {stats['total_hours']:.1f} hours\n")
                f.write(f"Trend:               {stats['trend']}\n\n")
                
                f.write("DAILY BREAKDOWN\n")
                f.write("-"*60 + "\n")
                for entry in data:
                    f.write(f"{entry['date']}: {entry['minutes']:.1f} minutes\n")
            
            print_success(f"Report exported to {REPORT_FILE}")
            
        except Exception as e:
            print_error(f"Error exporting report: {e}")

def show_menu():
    """Display main menu"""
    print(f"\n{Fore.MAGENTA}{Style.BRIGHT}{'='*60}")
    print(f"{'🧠 OVERTHINKING METER':^60}")
    print(f"{'='*60}{Style.RESET_ALL}")
    print(f"{Fore.CYAN}1.{Style.RESET_ALL} 📝 Log Overthinking Episode")
    print(f"{Fore.CYAN}2.{Style.RESET_ALL} 📜 View History")
    print(f"{Fore.CYAN}3.{Style.RESET_ALL} 🔍 Analyze My Patterns")
    print(f"{Fore.CYAN}4.{Style.RESET_ALL} 📊 Weekly Summary Report")
    print(f"{Fore.CYAN}5.{Style.RESET_ALL} 📈 Analyze Daily CSV Data")
    print(f"{Fore.CYAN}6.{Style.RESET_ALL} 📄 Export Full Report")
    print(f"{Fore.CYAN}7.{Style.RESET_ALL} 💡 Mental Health Tips")
    print(f"{Fore.CYAN}8.{Style.RESET_ALL} 🚪 Exit")
    print(f"{Fore.MAGENTA}{'─'*60}{Style.RESET_ALL}")

def show_mental_health_tips():
    """Display mental health and coping tips"""
    print_header("💡 MENTAL WELLNESS TIPS")
    
    tips = [
        ("🧘 Grounding Technique", "5-4-3-2-1: Name 5 things you see, 4 you can touch, 3 you hear, 2 you smell, 1 you taste"),
        ("📓 Journal", "Write down your thoughts to externalize them and reduce mental clutter"),
        ("🌬️ Breathing", "Box breathing: Inhale 4 counts, hold 4, exhale 4, hold 4. Repeat 5 times"),
        ("🚶 Movement", "A 10-minute walk can significantly reduce anxiety and clear your mind"),
        ("📵 Digital Detox", "Set boundaries with phone/social media, especially before bed"),
        ("🤝 Talk", "Share with a trusted friend, family member, or professional counselor"),
        ("😴 Sleep Hygiene", "Maintain consistent sleep schedule, avoid screens 1hr before bed"),
        ("🎯 Present Moment", "Ask yourself: 'Is this thought about the past, present, or future?'")
    ]
    
    for title, tip in tips:
        print(f"\n{Fore.GREEN}{Style.BRIGHT}{title}{Style.RESET_ALL}")
        print(f"  {tip}")
    
    print(f"\n{Fore.YELLOW}Remember: Seeking professional help is a sign of strength, not weakness!{Style.RESET_ALL}")
    print(f"{Fore.CYAN}If overthinking severely impacts your life, consider speaking with a counselor.{Style.RESET_ALL}")

def main():
    """Main program loop"""
    # Check for dry-run mode
    dry_run = '--dryrun' in sys.argv or '--dry-run' in sys.argv
    
    tracker = OverthinkingTracker(dry_run=dry_run)
    
    # Welcome screen
    print(f"{Fore.MAGENTA}{Style.BRIGHT}")
    print("╔═══════════════════════════════════════════════════════════╗")
    print("║                                                           ║")
    print("║              🧠 OVERTHINKING METER v1.0 🧠                ║")
    print("║                                                           ║")
    print("║        Track, Analyze & Reduce Your Overthinking          ║")
    print("║                                                           ║")
    print("╚═══════════════════════════════════════════════════════════╝")
    print(Style.RESET_ALL)
    print(f"{Fore.CYAN}💙 Remember: You're not alone. Mental wellness matters! 💙{Style.RESET_ALL}")
    
    while True:
        try:
            show_menu()
            choice = input(f"\n{Fore.YELLOW}Enter your choice (1-7): {Style.RESET_ALL}").strip()
            
            if choice == '1':
                tracker.log_overthinking()
            
            elif choice == '2':
                tracker.view_history()
            
            elif choice == '3':
                tracker.analyze_patterns()
            
            elif choice == '4':
                stats = DailyDataAnalyzer.analyze_daily_data()
                if stats:
                    main.last_stats = stats
                    main.last_data = DailyDataAnalyzer.read_daily_data(DAILY_DATA_FILE)
            
            elif choice == '5':
                if hasattr(main, 'last_stats') and hasattr(main, 'last_data'):
                    DailyDataAnalyzer.export_report(main.last_stats, main.last_data)
                else:
                    print_warning("Please analyze daily data first (option 4)")
            
            elif choice == '6':
                show_mental_health_tips()
            
            elif choice == '7':
                print_header("👋 TAKE CARE!")
                print_success("Remember: Be kind to yourself! 🌟")
                print_info("Your mental health matters. Keep tracking, keep improving! 💪")
                break
            
            else:
                print_error("Invalid choice. Please enter 1-7")
        
        except KeyboardInterrupt:
            print(f"\n\n{Fore.YELLOW}Interrupted by user{Style.RESET_ALL}")
            print_info("Exiting gracefully... Take care! 💙")
            break
        
        except Exception as e:
            print_error(f"An unexpected error occurred: {e}")
            print_info("The program will continue running...")

if __name__ == "__main__":
    main()