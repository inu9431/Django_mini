# 💰 가계부 미니 프로젝트 가이드

## 🎯 프로젝트 구조

> **1차 목표: MVP + 배포** → 빨리 끝난 사람은 도전 미션 진행

---

# ✅ MVP (필수 완성)

> 6일 안에 반드시 완성해야 하는 핵심 기능

---

## 1단계 — 환경 세팅

### 🐳 Docker

- Docker + PostgreSQL 연동

### 📦 의존성 관리

- uv로 패키지 관리

### 🔀 GitHub 협업

- 브랜치 전략 수립
- 협업 규칙 정리

---

## 2단계 — 모델 설계

### 📐 ERD

- ERD 설계

### 🗄️ 마이그레이션

- 모델 생성 및 마이그레이션

---

## 3단계 — 핵심 API

### 📋 API 스펙 설계

- 모든 기능(회원가입, 로그인, 로그아웃, 데이터 CRUD 등)의 엔드포인트, 메서드, 요청/응답 예시, 상태코드를 상세히 정리한다.
- 노션/구글 시트에 문서화하거나 코드로 직접 작성한다.
- RESTful API 설계 원칙을 참고한다.

> **API View 클래스 선택 기준 (앱별)**
>
> ### APIView 사용 (직접 구현)
> - **users 앱**: 회원가입, 로그인, 로그아웃, 회원정보 수정/삭제
>   - 이유: 로그인은 인증 → 토큰 생성 → 쿠키 세팅, 로그아웃은 쿠키 삭제 + 블랙리스트 처리 등 커스텀 흐름이 필요해서 Generic View 틀에 맞지 않음
> - **accounts 앱**: 계좌 CRD (생성/조회/삭제)
>   - 이유: 학습 목적으로 객체 조회, 권한 체크, 시리얼라이저 호출, 에러 처리를 직접 구현해본다
>
> ### Generic View 사용 (DRF 내장 활용)
> - **transactions 앱**: 거래내역 CRUD + 필터링
>   - 이유: 정형화된 CRUD + 필터링이라 Generic View가 적합하고, 6일 내 MVP 완성을 위해 효율적으로 구현한다
>   - 사용 클래스: `ListCreateAPIView`, `RetrieveUpdateDestroyAPIView`
>   - 오버라이드 필수 포인트:
>     - `get_queryset()`: 본인 거래내역만 필터링 (기본은 전체 반환이므로 오버라이드 필요)
>     - `perform_create()`: request.user를 거래내역에 자동 연결
>   - **원칙: 오버라이드 시 반드시 원본 메서드의 역할을 확인한 후 작성할 것**

### 🔐 인증 (회원가입 / 로그인 / 로그아웃)

**플로우차트**
- 인증 흐름(회원가입→로그인→로그아웃)을 시각화한다.
- 플로우차트를 `README.md`에 설명과 함께 삽입한다.

**회원가입**
- `CustomUser Model` 생성 + 이메일 인증 포함
- 비밀번호 암호화 저장

**로그인**
- SimpleJWT 설정 + JWT 인증을 기본 인증으로 설정
- Cookie에 토큰 저장 방식으로 구현

**로그아웃**
- Refresh Token을 블랙리스트에 추가

**회원정보 관리**
- 본인 프로필에만 접근 가능하도록 권한 제한
- PUT/PATCH 차이를 이해하고 수정 기능 구현
- 유저 삭제 시 "Deleted successfully" 응답 반환

### 🛡️ Django Admin

- admin.py에 User 모델 등록
- 이메일, 닉네임, 휴대폰번호로 검색 기능
- `is_staff`, `is_active` 기준 필터링
- 어드민 여부는 읽기 전용

### 💳 계좌 API (CRD)

**생성** — 사용자는 여러 개의 계좌를 등록할 수 있다.
**조회** — 계좌 정보는 생성 이후 수정 불가
**삭제** — 등록된 계좌를 삭제할 수 있다.

### 💸 거래내역 API (CRUD + 필터링)

**생성** — 거래내역을 생성할 수 있다.
**조회** — 모든 거래 내역을 조회할 수 있다.
**수정/삭제** — 거래 정보를 수정하거나 삭제할 수 있다.
**필터링** — 거래 유형, 거래 금액 등 2개 이상의 필터링 조건
**필수 조회 데이터** — 거래 계좌, 거래유형(입금/출금), 거래 금액, 거래 일시

### 🔗 URL 매핑

- 각 App별 urls.py 생성 → View를 URL에 매핑
- config/urls.py에서 `include`로 등록

### 📄 API 문서화 (Swagger)

- Swagger UI 설치 + 자동 문서화 설정
- `/docs` 또는 `/swagger-ui`에서 문서 확인
- 엔드포인트별 설명, 예시 요청/응답, 상태 코드 작성

---

## 4단계 — 품질

### ⚡ ORM 쿼리 최적화

**N+1 문제 해결**
- `select_related` / `prefetch_related` 활용
- 최적화 전후 쿼리 수 비교 → README.md에 정리

**쿼리 최적화 패턴**
- `annotate`, `aggregate`, `values`, `only`, `defer` 사용
- 사용 사례를 코드 예시와 함께 README.md에 정리

**쿼리 성능 모니터링**
- `django-debug-toolbar` 설치
- 쿼리 개수/수행 시간 시각화, 개선 전후 비교 → README.md에 기록

### 🧪 테스트 코드

- Accounts(계좌) 모델 CRUD TestCode 작성
- Transactions(거래내역) 모델 CRUD TestCode 작성

---

## 5단계 — 배포

### ⚙️ CI/CD (GitHub Actions)

**워크플로우 파일**
- `.github/workflows/build.yml` — CI (빌드 + Docker Hub 푸시)
- `.github/workflows/deploy.yml` — CD (EC2 배포)

**GitHub Secrets**
- `DOCKER_USERNAME`, `DOCKER_PASSWORD`
- `EC2_PRIVATE_KEY`, `EC2_HOST`, `EC2_USER`

### ☁️ AWS EC2

**인스턴스 생성**
- 프리 티어 `t2.micro` 활용
- 보안그룹 인바운드 80포트 확인

**인스턴스 접속 (SSH)**
- AWS 콘솔 또는 터미널로 접속

**코드 배포**
- EC2에 Git 설치 → 배포 브랜치 clone
- .env 파일 작성 (DB 정보, 시크릿 키 등)

### 🐋 Docker 배포

**EC2에서 빌드**
- Docker 설치 → 이미지 생성 → 컨테이너 실행 → API 테스트

**Docker Hub 연동**
- 이미지 태그 → Docker Hub Push
- EC2에서 Pull → 백그라운드 컨테이너 실행 → 정상 동작 확인

### 🔧 (선택) 추가 인프라

**RDS**
- PostgreSQL 생성 → 인바운드 규칙 편집 → DB 관리도구 연결 테스트 → 로컬 연결 테스트

**Nginx + Gunicorn**
- Nginx 설치 + 설정파일 작성
- Gunicorn 설치 + Django 연동
- `http://ec2.public.ip/<endpoint>` 접근 확인

---

# 🚀 도전 미션 1단계 (시간 남는 팀)

> MVP + 배포 완성 후 도전

---

### 🕐 wait_for_db

- Docker 환경에서 DB 준비 상태를 확인하는 management command 구현

### 📊 데이터 시각화 + Celery 스케줄링

**Analysis 앱**
- Analysis 모델 생성 (user, about, type, period_start, period_end, description, result_image, created_at, updated_at)

**Analyzer 구현**
- Pandas로 거래내역 데이터프레임 생성
- Matplotlib로 시각화 → 이미지 저장 → Analysis 모델 생성
- Analyzer Test Code 작성

**Analysis API**
- 분석 결과 리스트 반환 API View
- 쿼리 파라미터로 기간별(주간/월간) 필터링
- API Test Code 작성

**Celery 스케줄링**
- celery + django-celery-beat + django-celery-results 설치 및 설정
- analysis/tasks.py에 분석 Task 생성 → 스케줄링 등록
- 백그라운드 실행 확인 → 결과물 README.md에 작성

### 🔔 알림 기능 (Django Signal)

**Notification 모델**
- user(FK), message, is_read, created_at

**Notification API**
- 미확인 알림 리스트 조회
- 알림 읽기 (pk로 `is_read` → True)
- Test Code 작성

**Signal 연동**
- Analysis 모델 `post_save` → 알림 자동 생성

---

# 🔥 도전 미션 2단계 (상위 팀)

> 도전 1단계 완성 후 도전

---

### 🌐 Social Login (OAuth)

**분석**
- Google / Naver / Kakao 중 하나 이상 선택
- OAuth 인증 로직 분석 → README.md에 작성

**설정**
- 선택 플랫폼 개발자 사이트에서 OAuth API 설정
- Access Key, Secret Key, Callback URI 환경변수 지정

**구현**
- django-allauth provider 사용 또는 직접 Social Login View 구현

### 🔄 TDD 리팩토링

- 기존 코드를 TDD 방식으로 리팩토링

---

# 📊 팀별 목표 기준

| 수준 | 목표 |
| --- | --- |
| 프레임워크 익숙하지 않은 팀 | MVP만 완성 (배포 제외 가능) |
| 어느 정도 이해한 팀 | **MVP + 배포 (1차 목표)** |
| 자신 있는 팀 | MVP + 배포 + 도전 1단계 |
| 상위 팀 | MVP + 배포 + 도전 1~2단계 |

---

# ⚠️ 주의사항

- **MVP + 배포**가 최우선 → 완성 후 순서대로 도전 미션 진행
- 도전 미션은 선택사항, 미완성이어도 감점 없음
- Social Login / Celery / 알림은 난이도 높음 → 무리하지 말 것
- 6일 기준 **MVP + 배포**까지가 현실적인 목표