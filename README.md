# Spotify Money Calculator 💿💰

**Calculate how much it would cost to own your Spotify liked songs collection physically**

Ever wondered how much money you'd need to buy all your favorite Spotify songs on physical media? This project connects to your Spotify account, analyzes your liked songs, and calculates the cost of building the same collection with CDs, vinyl records, or other physical formats.

## 🎯 Project Status

Currently in early development! The project currently implements:
- ✅ Spotify OAuth authentication flow
- ✅ FastAPI-based REST API
- 🚧 Liked songs retrieval (in progress)
- 🚧 Cost calculation engine (planned)
- 🚧 Physical format pricing (planned)

## 🛠️ Tech Stack

- **Framework**: [FastAPI](https://fastapi.tiangolo.com/) - Modern, fast web framework for building APIs
- **Language**: Python 3.13+
- **HTTP Client**: [httpx](https://www.python-httpx.org/) - Async HTTP client for Spotify API calls
- **Validation**: [Pydantic](https://docs.pydantic.dev/) - Data validation and settings management
- **Server**: [Uvicorn](https://www.uvicorn.org/) - Lightning-fast ASGI server
- **Package Manager**: [uv](https://github.com/astral-sh/uv) - Fast Python package installer

## 📋 Prerequisites

Before you begin, ensure you have the following installed:

- **Python 3.13** or higher
- **uv** package manager ([installation guide](https://github.com/astral-sh/uv))
- **Spotify Developer Account** - Create one at [developer.spotify.com](https://developer.spotify.com/)

## 🚀 Installation

1. **Clone the repository**
   ```bash
   git clone https://github.com/yourusername/spotify_money_calculator.git
   cd spotify_money_calculator
   ```

2. **Install dependencies**
   ```bash
   uv sync
   ```

3. **Set up environment variables**
   
   Create a `.env` file in the project root:
   ```env
   SPOTIFY_CLIENT_ID=your_spotify_client_id
   SPOTIFY_CLIENT_SECRET=your_spotify_client_secret
   SPOTIFY_REDIRECT_URI=your_redirect_uri
   SPOTIFY_STATE=your_random_state_string
   ```

## ⚙️ Configuration

### Spotify API Setup

1. Go to [Spotify Developer Dashboard](https://developer.spotify.com/dashboard)
2. Create a new application
3. Copy your **Client ID** and **Client Secret**
4. Add your redirect URI to the app settings (e.g., `http://localhost:8888/api/v0/spotify/callback`)
5. Update the redirect URL in `router.py` or use environment variables

### Environment Variables

| Variable | Description | Required |
|----------|-------------|----------|
| `SPOTIFY_CLIENT_ID` | Your Spotify app client ID | Yes |
| `SPOTIFY_CLIENT_SECRET` | Your Spotify app client secret | Yes |
| `SPOTIFY_REDIRECT_URI` | OAuth callback URL | Yes |
| `SPOTIFY_STATE` | Random string for OAuth state verification | Yes |
| `SPOTIFY_SCOPE` | Spotify API scopes (default: `user-read-private user-read-email`) | No |

## 🎮 Usage

### Running the Application

Start the development server:
```bash
make run
```

The API will be available at `http://localhost:8888`

### API Endpoints

#### Health Check
```
GET /api/v0/spotify/
```
Returns a simple "Hello World" message to verify the API is running.

#### Initiate Spotify Login
```
GET /api/v0/spotify/login
```
Redirects to Spotify's OAuth authorization page. Users will be asked to grant permissions to access their Spotify data.

#### OAuth Callback
```
GET /api/v0/spotify/callback?code={code}&state={state}
```
Handles the OAuth callback from Spotify. Exchanges the authorization code for an access token.

**Response**: Returns `"OAuth Flow completed successfully"` on success.

### Example Flow

1. Start the server: `make run`
2. Navigate to: `http://localhost:8888/api/v0/spotify/login`
3. Authorize the application in Spotify
4. Get redirected back to the callback endpoint
5. Access token is retrieved (ready for future API calls)

## 🔧 Development

### Available Commands

The project uses a Makefile for common development tasks:

```bash
make run        # Run the application
make format     # Format code with ruff
make lint       # Run linter with auto-fix
make check-lint # Check linting without fixes
make check      # Format + lint check
make help       # Show all available commands
```

### Code Style

This project uses [Ruff](https://github.com/astral-sh/ruff) for both formatting and linting:
- **Formatting**: Consistent code style across the project
- **Linting**: Catch common errors and enforce best practices

Run `make check` before committing to ensure code quality.

## 🗺️ Roadmap

### Phase 1: Data Collection ✅ (In Progress)
- [x] Spotify OAuth authentication
- [ ] Fetch user's liked songs
- [ ] Retrieve song metadata (artist, album, year)
- [ ] Handle pagination for large collections

### Phase 2: Cost Calculation Engine
- [ ] Define physical format types (CD, Vinyl, Cassette)
- [ ] Integrate pricing APIs or databases
- [ ] Calculate costs per song/album
- [ ] Aggregate total collection cost
- [ ] Handle special cases (compilations, box sets)

### Phase 3: User Experience
- [ ] Web frontend for results visualization
- [ ] Breakdown by format type
- [ ] Breakdown by artist/album
- [ ] Cost comparisons (streaming vs. physical)
- [ ] Export reports (PDF, CSV)

### Phase 4: Advanced Features
- [ ] Historical pricing trends
- [ ] Rare/out-of-print album identification
- [ ] Regional pricing variations
- [ ] Condition-based pricing (new, used, collectible)

## 📁 Project Structure

```
spotify_money_calculator/
├── main.py              # Application entry point
├── router.py            # API routes and Spotify OAuth logic
├── pyproject.toml       # Project metadata and dependencies
├── Makefile            # Development commands
├── .env                # Environment variables (not in repo)
├── .gitignore          # Git ignore rules
└── README.md           # This file
```

## 🤝 Contributing

Contributions are welcome! This is an early-stage project with lots of room for improvement.

### How to Contribute
1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Make your changes
4. Run `make check` to ensure code quality
5. Commit your changes (`git commit -m 'Add amazing feature'`)
6. Push to the branch (`git push origin feature/amazing-feature`)
7. Open a Pull Request

## 📝 License

This project is open source and available under the [MIT License](LICENSE).

## 🙏 Acknowledgments

- [Spotify Web API](https://developer.spotify.com/documentation/web-api/) for making this possible
- The FastAPI community for excellent documentation
- Everyone who's ever wondered about the real cost of their music collection

---

**Note**: This project is for educational and entertainment purposes. Prices are estimates and may not reflect actual market values. Always support artists by purchasing music through legitimate channels!
