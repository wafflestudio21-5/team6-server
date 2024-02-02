<a name="team6-server-top"></a>

[![Contributors][contributors-shield]][contributors-url]
[![Commits][commits-shield]][commits-url]
[![pr][pr-shield]][pr-url]
[![cpr][cpr-shield]][cpr-url]


<!-- PROJECT LOGO -->
<br />
<div align="center">
  <a href="https://wafflestudio.com/">
    <img src="https://wafflestudio.com/static/images/logo/pupuri_logo.png" alt="Logo">
  </a>
  <a href="https://github.com/wafflestudio21-5/team6-server">
    <img src="https://oopy.lazyrockets.com/api/v2/notion/image?src=https%3A%2F%2Fs3-us-west-2.amazonaws.com%2Fsecure.notion-static.com%2Ffc327ed6-4e98-4bfc-a3b9-86d14dbc3245%2FWATCHA_PEDIA_LOGO.svg&blockId=314b8d15-5712-454d-b22e-37c72f131885" alt="Logo">
  </a>

  <h3 align="center">와플피디아-서버</h3>

  <p align="center">
    와플스튜디오 루키 21.5기 팀6 와플피디아 프로젝트의 서버팀
    <br />
    <br />
    <a href="https://d1vexdz72u651e.cloudfront.net/">View Demo</a>
    ·
    <a href="https://docs.google.com/forms/d/e/1FAIpQLSd1rREhQ2cB_LWTdKe6OV-6C8jC3X7AcXKRlx5Xw_sm-0Fskg/viewform?usp=sf_link">Report Bug</a>
  </p>
</div>



<!-- TABLE OF CONTENTS -->
<details>
  <summary>Table of Contents</summary>
  <ol>
    <li>
      <a href="#about-the-project">About The Project</a>
      <ul>
        <li><a href="#WafflePedia">WafflePedia</a></li>
        <li><a href="#Deployment">Deployment</a></li>
        <li><a href="#Stacks">Stacks</a></li>
      </ul>
    </li>
    <li>
      <a href="#Development">Development</a>
      <ul>
        <li><a href="#Contributors">Contributors</a></li>
        <li><a href="#Roadmap">Roadmap</a></li>
      </ul>
    </li>
    <li><a href="#contact">Contact</a></li>
    <li><a href="#acknowledgments">Acknowledgments</a></li>
  </ol>
</details>



<!-- ABOUT THE PROJECT -->
## About The Project

### WafflePedia

🧇[**와플피디아**](https://d1vexdz72u651e.cloudfront.net/) 는 [**왓챠피디아 웹사이트**](https://pedia.watcha.com/ko-KR/)의 클론 프로젝트입니다! 기존의 왓챠피디아는 영화와 책, TV 프로그램에 대해 추천을 받을 수 있고, 자신의 관람평과 별점을 공유하여 다른 유저와 소통하는 **콘텐츠 추천 & 의견 커뮤니티 웹서비스** 입니다. 저희 TEAM6 팀원들은 개발기간과 서로의 역량을 고려하여, 와플피디아를 **영화 콘텐츠에 대한 의견 커뮤니티 서비스**에 집중하는, 그러나 핵심적이고 필수적인 기능들을 내실 있게 제공하는 웹서비스로 완성하고자 하였습니다. 많이 부족하지만 열과 성을 다해 제작한 저희 와플피디아 서비스를 만족스럽게 사용하실 수 있기를 바랍니다🙏🙏

개발 기간 : 23.12.28 ~ 24.02.02

\*본 레포는 **TEAM6-SERVER REPO** 이므로 BACKEND 개발에 관한 내용을 위주로 설명합니다.

FRONTEND 개발에 관해 궁금하다면? [TEAM6-WEB REPO](https://github.com/wafflestudio21-5/team6-web)
<br/><br/>

### Deployment

프론트엔드 서버 도메인(Web server) : <https://d1vexdz72u651e.cloudfront.net/>

백엔드 서버 도메인(Api server) : <https://wafflepedia.xyz/>

### Stacks

#### 기술 스택

<img src="https://img.shields.io/badge/Django-092E20?style=for-the-badge&logo=django&logoColor=green"> &nbsp; &nbsp; &nbsp;
<img src="https://img.shields.io/badge/Amazon EC2-FF9900?style=for-the-badge&logo=Amazon EC2&logoColor=white"> &nbsp; &nbsp; &nbsp;
<img src="https://img.shields.io/badge/Amazon RDS-527FFF?style=for-the-badge&logo=Amazon RDS&logoColor=white"> &nbsp; &nbsp; &nbsp;
<img src="https://img.shields.io/badge/Amazon S3-569A31?style=for-the-badge&logo=Amazon S3&logoColor=white"> 

#### 협업

<img src="https://img.shields.io/badge/Slack-4A154B?style=for-the-badge&logo=Slack&logoColor=white"> &nbsp; &nbsp; &nbsp;
<img src="https://img.shields.io/badge/Notion-000000?style=for-the-badge&logo=Notion&logoColor=white"> &nbsp; &nbsp; &nbsp;

<br/>

<!-- Development -->
## Development

### Contributors

#### 인증 | 유저
<img src="https://img.shields.io/badge/%EC%9D%B4%EB%8B%A4%EC%9D%80-de--yi-blue?style=plastic&link=https%3A%2F%2Fgithub.com%2Fde-yi"> &nbsp; &nbsp;
<img src="https://img.shields.io/badge/%EA%B0%95%EC%9A%B0%EC%A7%84-woojin--blaze-blue?style=plastic&link=https%3A%2F%2Fgithub.com%2Fwoojin-blaze">

- Json Web Token 이용 유저 인증 구현
- 소셜 로그인(카카오) 구현
- 유저 팔로우/언팔로우 구현
- 유저 개별페이지 구현
<br/><br/>

#### 컨텐츠 | 게시물
<img src="https://img.shields.io/badge/%EC%9D%B4%EA%B7%9C%EC%9B%90-civilian38-orange?style=plastic&link=https%3A%2F%2Fgithub.com%2Fcivilian38"> &nbsp; &nbsp;
<img src="https://img.shields.io/badge/%EB%B0%B1%EC%B0%BD%EC%9D%B8-nuagenic-orange?style=plastic&link=https%3A%2F%2Fgithub.com%2Fnuagenic">

- 모델 설계 및 ERD 작성
- 주요 기능 CRUD 구현
- Kobis/KMDB 로부터 영화 데이터 주입

<!-- ROADMAP -->
### Roadmap
> week1
> >공통
> > - [x] 프로젝트 셋업
> > - [x] AWS 연결
> > - [x] API 엔드포인트 초안 작성
> > - [x] 영화 DB 탐색
> > - [x] CI/CD 적용
>
> week2
> > 인증 | 유저
> >  - [x] 유저 인증 구현 시작
> 
> > 컨텐츠 | 게시물
> > - [x] 모델 설계 및 ERD 작성
> 
> week3
> > 인증 | 유저
> > - [x] RDS 연결
> > - [x] 유저 인증 구현 완료
> > - [x] 연결 문제 해결
> 
> > 컨텐츠 | 게시물
> > - [x] 영화 캐러셀 / 상세보기 View 구현
> > - [x] 영화 코멘트 CRUD 작업
> > - [x] 영화 DB 주입 시작
> 
> week4
> > 인증 | 유저
> > - [x] 소셜 로그인 구현
> > - [x] 유저 팔로우 / 언팔로우 구현
> 
> > 컨텐츠 | 게시물
> > - [x] 영화 평점 CRUD 작업
> > - [x] 코멘트 댓글 CRUD 작업
> > - [x] 코멘트 / 댓글 좋아요 작업
> 
> week5
> > 인증 | 유저
> > - [x] S3 연결
> > - [x] 유저 페이지 구현
>
> > 컨텐츠 | 게시물
> > - [x] 영화 DB 주입 마무리
> 
> week 6
> > 공통
> > - [ ] 버그픽스, 엔드포인트 수정

<!-- CONTACT -->
## Contact



<!-- ACKNOWLEDGMENTS -->
## Acknowledgments


<!-- MARKDOWN LINKS & IMAGES -->
<!-- https://www.markdownguide.org/basic-syntax/#reference-style-links -->
[contributors-shield]: https://img.shields.io/github/contributors/wafflestudio21-5/team6-server.svg?style=for-the-badge
[contributors-url]: https://github.com/wafflestudio21-5/team6-server/graphs/contributors
[commits-shield]: https://img.shields.io/github/commit-activity/t/wafflestudio21-5/team6-server?style=for-the-badge&link=https%3A%2F%2Fgithub.com%2Fwafflestudio21-5%2Fteam6-server%2Fcommits%2Fmain%2F
[commits-url]: https://github.com/wafflestudio21-5/team6-server/commits/main/
[pr-shield]: https://img.shields.io/github/issues-pr/wafflestudio21-5/team6-server?style=for-the-badge&link=https%3A%2F%2Fgithub.com%2Fwafflestudio21-5%2Fteam6-server%2Fpulls
[pr-url]: https://github.com/wafflestudio21-5/team6-server/pulls
[cpr-shield]: https://img.shields.io/github/issues-pr-closed/wafflestudio21-5/team6-server?style=for-the-badge&link=https%3A%2F%2Fgithub.com%2Fwafflestudio21-5%2Fteam6-server%2Fpulls%3Fq%3Dis%253Apr%2Bis%253Aclosed
[cpr-url]: https://github.com/wafflestudio21-5/team6-server/pulls?q=is%3Apr+is%3Aclosed
