from django.test import TestCase, Client
from bs4 import BeautifulSoup
from .models import Post

# Create your tests here.

class TestView(TestCase):
    def setUp(self):
        self.client = Client()

    def test_post_list(self):
        response = self.client.get('/blog/')
        self.assertEqual(response.status_code, 200)
        soup = BeautifulSoup(response.content, 'html.parser')
        self.assertEqual(soup.title.text, 'Blog')

        navbar = soup.nav
        self.assertIn('Do It 장고', navbar.text)

        print(Post.objects.count())
        self.assertEqual(Post.objects.count(), 0)

        main_area = soup.find('div', id="main-area")
        self.assertIn('아직 게시물이 없습니다.', main_area.text)


        # test 에서 Post.objects.create( ) 호출하면 임시로 생성되고
        # 함수가 종료되면 사라지므로 사라지기전에 사이트를 호출해서 확인 함.
        post_001 = Post.objects.create(
            title='나 장고 두번째',
            content= "반갑다 꼭 통과해라.... "
        )
        response = self.client.get('/blog/')
        self.assertEqual(response.status_code,200);
        soup = BeautifulSoup(response.content, 'html.parser')
        main_area = soup.find('div', id='main-area')

        self.assertIn(post_001.title, main_area.text)

    def test_post_detail(self):
        post_001 = Post.objects.create(
            title = '첫번째 포트스입니다.',
            content ='안녕.... 반가워.'
        )
        post_002 = Post.objects.create(
            title = '두번째 포트스입니다.',
            content ='안녕.... 반가워.'
        )
        self.assertEqual(post_001.get_absolute_url(), '/blog/1/')
        response = self.client.get(post_001.get_absolute_url())
        self.assertEqual(response.status_code, 200)
        soup = BeautifulSoup(response.content, 'html.parser')
        navbar = soup.nav
        self.assertIn('Do It 장고', navbar.text)
        self.assertIn(post_001.title, soup.title.text)

        main_area = soup.find('div', id='main-area')
        post_area = main_area.find('div', id='post-area')
        self.assertIn(post_001.title, post_area.text)


