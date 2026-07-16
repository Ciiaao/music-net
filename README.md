# 🎵 Music Platform — Django REST API

A full-featured music streaming & social platform built with Django, Django REST Framework, and Django Channels.

---

## ✅ Features

- **User Accounts**: Register, login (JWT), profile, follow/unfollow, privacy settings
- **Music**: Upload songs (auto-extracts duration), artists, albums, genres, play counter, live "Now Playing"
- **Playlists**: Create/edit/delete, add/remove songs, public or private
- **Feed**: Posts (share songs/playlists or text requests), likes, comments, shares
- **Discovery**: Trending posts feed
- **Search**: Global search across songs, playlists, artists, users
- **Real-time Chat**: 1-to-1 private chat, group chats with admin management, share songs in messages (WebSocket)
- **Notifications**: Follow, like, comment notifications + real-time via WebSocket
- **Admin Panel**: Ban/unban users, approve/remove songs and posts

---

## 🚀 Setup

### 1. Clone & create virtualenv
```bash
python -m venv venv
source venv/bin/activate        # Windows: venv\Scripts\activate
pip install -r requirements.txt
```

### 2. Configure environment
```bash
cp .env.example .env
# Edit .env with your settings
```

### 3. Run migrations
```bash
python manage.py makemigrations accounts music playlists feed chat notifications
python manage.py migrate
```

### 4. Create superuser
```bash
python manage.py createsuperuser
```

### 5. Start the server

**Development (HTTP only — no WebSocket):**
```bash
python manage.py runserver
```

**Development with WebSocket support:**
```bash
# Install daphne first: pip install daphne
daphne -b 0.0.0.0 -p 8000 config.asgi:application
```

**For real-time chat & notifications, also start Redis:**
```bash
redis-server
```
Then update `config/settings/base.py` CHANNEL_LAYERS to use Redis:
```python
CHANNEL_LAYERS = {
    'default': {
        'BACKEND': 'channels_redis.core.RedisChannelLayer',
        'CONFIG': {'hosts': [('127.0.0.1', 6379)]},
    }
}
```

---

## 📖 API Documentation

Once the server is running, visit:
- **Swagger UI**: http://localhost:8000/api/docs/
- **ReDoc**: http://localhost:8000/api/redoc/
- **Django Admin**: http://localhost:8000/admin/

---

## 📋 API Endpoints

### Accounts
| Method | Endpoint | Description |
|--------|----------|-------------|
| POST | `/api/accounts/register/` | Register new user |
| POST | `/api/accounts/login/` | Login (get JWT) |
| POST | `/api/accounts/token/refresh/` | Refresh JWT |
| POST | `/api/accounts/logout/` | Logout (blacklist token) |
| GET/PATCH | `/api/accounts/me/` | Own profile |
| GET/PATCH | `/api/accounts/profile/<id>/` | User profile |
| POST | `/api/accounts/follow/<id>/` | Follow/unfollow toggle |
| GET | `/api/accounts/<id>/followers/` | Follower list |
| GET | `/api/accounts/<id>/following/` | Following list |

### Music
| Method | Endpoint | Description |
|--------|----------|-------------|
| GET/POST | `/api/music/songs/` | List / upload songs |
| GET/PUT/DELETE | `/api/music/songs/<id>/` | Song detail |
| POST | `/api/music/songs/<id>/play/` | Increment play count + set NowPlaying |
| GET | `/api/music/now-playing/<user_id>/` | User's current song |
| GET | `/api/music/now-playing/following/` | Followed users' current songs |
| GET/POST | `/api/music/artists/` | Artists |
| GET/POST | `/api/music/albums/` | Albums |
| GET/POST | `/api/music/genres/` | Genres |

### Playlists
| Method | Endpoint | Description |
|--------|----------|-------------|
| GET/POST | `/api/playlists/` | List / create playlists |
| GET | `/api/playlists/my/` | Own playlists |
| GET/PUT/DELETE | `/api/playlists/<id>/` | Playlist detail |
| POST/DELETE | `/api/playlists/<id>/songs/` | Add / remove song |

### Feed
| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/api/feed/` | Main feed (followed users) |
| GET | `/api/feed/discovery/` | Trending posts |
| GET/POST | `/api/feed/posts/` | All posts |
| GET/DELETE | `/api/feed/posts/<id>/` | Post detail |
| POST | `/api/feed/posts/<id>/like/` | Like / unlike toggle |
| GET/POST | `/api/feed/posts/<id>/comments/` | Comments |
| POST | `/api/feed/posts/<id>/share/` | Share post |
| GET | `/api/feed/user/<user_id>/posts/` | User's posts |

### Search
| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/api/search/?q=<query>` | Global search |

### Chat
| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/api/chat/rooms/` | My chat rooms |
| POST | `/api/chat/rooms/private/` | Start private chat |
| POST | `/api/chat/rooms/group/` | Create group chat |
| POST/DELETE | `/api/chat/rooms/<id>/members/` | Add/remove group member |
| GET/POST | `/api/chat/rooms/<id>/messages/` | Messages (HTTP fallback) |
| WS | `ws://host/ws/chat/<room_id>/` | Real-time chat WebSocket |

### Notifications
| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/api/notifications/` | All notifications |
| GET | `/api/notifications/unread/` | Unread count |
| POST | `/api/notifications/mark-all-read/` | Mark all as read |
| POST | `/api/notifications/<id>/read/` | Mark one as read |
| WS | `ws://host/ws/notifications/` | Real-time notifications |

---

## 🗂 Project Structure

```
music_platform/
├── manage.py
├── requirements.txt
├── .env.example
├── config/
│   ├── settings/base.py
│   ├── urls.py
│   └── asgi.py
└── apps/
    ├── accounts/     # Users, follow
    ├── music/        # Songs, albums, artists, genres
    ├── playlists/    # Playlist management
    ├── feed/         # Posts, likes, comments
    ├── search/       # Global search
    ├── chat/         # Real-time chat
    ├── notifications/# Notifications
    └── administration/ # Admin extensions
```

---

## 🔐 Authentication

All endpoints (except register/login) require a JWT Bearer token:

```
Authorization: Bearer <your_access_token>
```

**WebSocket authentication**: Pass the token as a query param:
```
ws://localhost:8000/ws/chat/1/?token=<access_token>
```
(You'll need to add a `QueryAuthMiddleware` for this — see Django Channels docs.)
