import logging
import requests
from bs4 import BeautifulSoup

logging.getLogger(__name__)

class StudentInfo:
    PROFILE_PAGE = r'https://code.ptit.edu.vn/user/profile'

    def __init__(self, name: str = 'Guest', student_id: str = 'None', klass: str = 'None'):
        self.name = name
        self.student_id = student_id
        self.klass = klass

class LoginRequest:
    LOGIN_PAGE = r'https://code.ptit.edu.vn/login'

    def __init__(self, username: str, password: str):
        self.username = username
        self.password = password
        self.session = requests.Session()
        self.session.headers.update({
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8',
            'Accept-Language': 'vi-VN,vi;q=0.9,en-US;q=0.8,en;q=0.7',
            'Referer': self.LOGIN_PAGE 
        })

    def attempt(self) -> StudentInfo:
        try:
            response = self.session.get(self.LOGIN_PAGE)
            soup = BeautifulSoup(response.text, 'html.parser')

            token_tag = soup.find('input', {'name': '_token'})
            if not token_tag:
                print("Không lấy được token")
                return None
            _token = token_tag['value']
            data = {
                '_token': _token,
                'username': self.username,
                'password': self.password,
            }
            request = self.session.post(self.LOGIN_PAGE, data=data, allow_redirects=True)
            print("URL sau login:", request.url)
            profile = self.session.get(StudentInfo.PROFILE_PAGE)

            if "login" in profile.url:
                print("Login thất bại (redirect về login)")
                return None

            soup = BeautifulSoup(profile.text, 'html.parser')

            name_tag = soup.find('p', {'class': 'profile__name'})
            if not name_tag:
                print("Không lấy được profile")
                return None

            name = name_tag.get_text(strip=True)
            spans = soup.select('p.profile__item__info__title span')

            student_id = spans[0].get_text(strip=True) if len(spans) > 0 else 'N/A'
            klass = spans[1].get_text(strip=True) if len(spans) > 1 else 'N/A'

            return StudentInfo(name, student_id, klass)

        except Exception as e:
            print("Lỗi:", e)
            return None