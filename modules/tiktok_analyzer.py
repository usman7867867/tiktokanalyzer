"""TikTok username analyzer module."""
import re
import json
import os
import requests
from datetime import datetime
from bs4 import BeautifulSoup
from modules.ui import print_success, print_error, print_info, Spinner

class TikTokAnalyzer:
    def __init__(self, config, logger):
        self.config = config
        self.logger = logger
        self.data_dir = 'data'
        self.reports_dir = 'reports'

    def validate_username(self, username):
        """Validate TikTok username format."""
        pattern = r'^[a-zA-Z0-9._]{2,24}$'
        return re.match(pattern, username) is not None

    def fetch_profile(self, username):
        """
        Scrape publicly available profile info from TikTok user page.
        Returns dict with profile data or None on failure.
        """
        if not self.validate_username(username):
            raise ValueError("Invalid username format. Use 2-24 alphanumeric, underscore or dot.")

        url = f"https://www.tiktok.com/@{username}"
        headers = {
            "User-Agent": "Mozilla/5.0 (Linux; Android 10; K) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Mobile Safari/537.36"
        }
        try:
            self.logger.info(f"Fetching profile for @{username}")
            response = requests.get(url, headers=headers, timeout=10)
            response.raise_for_status()

            soup = BeautifulSoup(response.text, 'html.parser')
            # Try to find the SIGI_STATE JSON blob
            script_tag = soup.find('script', id='SIGI_STATE')
            if not script_tag:
                # Fallback to __UNIVERSAL_DATA_FOR_REHYDRATION__
                script_tag = soup.find('script', id='__UNIVERSAL_DATA_FOR_REHYDRATION__')

            if not script_tag or not script_tag.string:
                raise Exception("Could not locate user data on page (blocked or changed structure).")

            data = json.loads(script_tag.string)
            # Navigate to user info
            user_info = None
            if 'UserModule' in data:
                user_info = data['UserModule']['users'].get(username, {})
            elif '__DEFAULT_SCOPE__' in data:
                # TikTok's newer structure
                for key in data['__DEFAULT_SCOPE__']:
                    if 'webapp.user-detail' in key:
                        user_info = data['__DEFAULT_SCOPE__'][key].get('userInfo', {}).get('user', {})
                        break

            if not user_info:
                raise Exception("User data not found in page JSON.")

            profile = {
                'username': user_info.get('uniqueId', username),
                'nickname': user_info.get('nickname', ''),
                'bio': user_info.get('signature', ''),
                'followers': user_info.get('followerCount', 0),
                'following': user_info.get('followingCount', 0),
                'likes': user_info.get('heartCount', 0),
                'videos': user_info.get('videoCount', 0),
                'verified': user_info.get('verified', False),
                'avatar': user_info.get('avatarMedium', ''),
                'private': user_info.get('privateAccount', False),
                'region': user_info.get('region', '')
            }
            self.logger.info(f"Profile data fetched for @{username}")
            return profile

        except requests.RequestException as e:
            self.logger.error(f"Network error: {e}")
            raise Exception(f"Network error: {str(e)}")
        except Exception as e:
            self.logger.error(f"Scraping error: {e}")
            raise

    def save_analysis(self, username, profile):
        """Save analysis result as JSON and TXT in data/ and reports/."""
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        # Save raw data to data folder
        data_file = os.path.join(self.data_dir, f"{username}_{timestamp}.json")
        with open(data_file, 'w', encoding='utf-8') as f:
            json.dump(profile, f, indent=4, ensure_ascii=False)
        self.logger.info(f"Saved raw data to {data_file}")

        # Generate report in reports folder
        self.generate_report(username, profile, timestamp)

    def generate_report(self, username, profile, timestamp=None):
        """Generate JSON and TXT reports."""
        if timestamp is None:
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")

        # JSON report
        json_path = os.path.join(self.reports_dir, f"report_{username}_{timestamp}.json")
        with open(json_path, 'w', encoding='utf-8') as f:
            json.dump({
                'analyzed_at': timestamp,
                'username': username,
                'profile': profile
            }, f, indent=4, ensure_ascii=False)

        # TXT report
        txt_path = os.path.join(self.reports_dir, f"report_{username}_{timestamp}.txt")
        with open(txt_path, 'w', encoding='utf-8') as f:
            f.write(f"TikTok Profile Report for @{username}\n")
            f.write(f"Generated: {timestamp}\n")
            f.write("="*50 + "\n")
            f.write(f"Nickname    : {profile['nickname']}\n")
            f.write(f"Bio         : {profile['bio']}\n")
            f.write(f"Followers   : {profile['followers']:,}\n")
            f.write(f"Following   : {profile['following']:,}\n")
            f.write(f"Likes       : {profile['likes']:,}\n")
            f.write(f"Videos      : {profile['videos']}\n")
            f.write(f"Verified    : {'Yes' if profile['verified'] else 'No'}\n")
            f.write(f"Private     : {'Yes' if profile['private'] else 'No'}\n")
            f.write(f"Region      : {profile['region']}\n")
            f.write(f"Avatar URL  : {profile['avatar']}\n")

        self.logger.info(f"Reports generated: {json_path}, {txt_path}")
        return json_path, txt_path

    def analyze_username(self, username):
        """Full analysis flow with spinner."""
        if not self.validate_username(username):
            print_error("Invalid username. Must be 2-24 alphanumeric, underscore or dot.")
            return

        with Spinner("Fetching profile data..."):
            try:
                profile = self.fetch_profile(username)
            except Exception as e:
                print_error(f"Failed to fetch profile: {e}")
                return

        # Display result
        print_success(f"\nProfile for @{username}:")
        print(f"  Nickname    : {profile['nickname']}")
        print(f"  Bio         : {profile['bio'][:100]}{'...' if len(profile['bio'])>100 else ''}")
        print(f"  Followers   : {profile['followers']:,}")
        print(f"  Following   : {profile['following']:,}")
        print(f"  Likes       : {profile['likes']:,}")
        print(f"  Videos      : {profile['videos']}")
        print(f"  Verified    : {'Yes' if profile['verified'] else 'No'}")
        print(f"  Private     : {'Yes' if profile['private'] else 'No'}")
        print(f"  Region      : {profile['region']}")
        print(f"  Avatar      : {profile['avatar']}")

        # Save results
        self.save_analysis(username, profile)
        print_success("Analysis saved to data/ and reports/")
