# Spotify Money Calculator 💿💰

**Calculate how much it would cost to own your Spotify liked songs collection physically**

Ever wondered how much money you'd need to buy all your favorite Spotify songs on physical media? This project connects to your Spotify account, analyzes your liked songs, and calculates the cost of building the same collection with CDs, vinyl records, or other physical formats.

## 🎯 Project Status

The project is now functional with core features implemented! 

### What's Working:
- ✅ Spotify OAuth authentication flow with cookie-based session management
- ✅ FastAPI-based REST API
- ✅ User saved albums retrieval with pagination support
- ✅ **Discogs API integration for physical album pricing**
- ✅ **Cost calculation engine for CD prices**
- ✅ **Interactive web frontend with album display**
- ✅ Real-time price aggregation and summary

### What's Next:
- 🚧 Vinyl and cassette pricing options
- 🚧 Full liked songs (tracks) retrieval
- 🚧 Enhanced price accuracy and search results
- 🚧 Export functionality (PDF, CSV)

## 🛠️ Tech Stack

- **Framework**: [FastAPI](https://fastapi.tiangolo.com/) - Modern, fast web framework for building APIs
- **Language**: Python 3.13+
- **HTTP Client**: [httpx](https://www.python-httpx.org/) - Async HTTP client for Spotify API calls
- **Validation**: [Pydantic](https://docs.pydantic.dev/) - Data validation and settings management
- **Server**: [Uvicorn](https://www.uvicorn.org/) - Lightning-fast ASGI server
- **Package Manager**: [uv](https://github.com/astral-sh/uv) - Fast Python package installer
- **Pricing API**: [Discogs API](https://www.discogs.com/developers/) - Physical music marketplace data
- **Template Engine**: [Jinja2](https://jinja.palletsprojects.com/) - HTML templating

## 📋 Prerequisites

Before you begin, ensure you have the following installed:

- **Python 3.13** or higher
- **uv** package manager ([installation guide](https://github.com/astral-sh/uv))
- **Spotify Developer Account** - Create one at [developer.spotify.com](https://developer.spotify.com/)
- **Discogs Developer Account** - Create one at [discogs.com/developers](https://www.discogs.com/developers/)

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
   SPOTIFY_SCOPE=user-library-read
   DISCOGS_ACCESS_TOKEN=your_discogs_personal_access_token
   ```

## ⚙️ Configuration

### Spotify API Setup

1. Go to [Spotify Developer Dashboard](https://developer.spotify.com/dashboard)
2. Create a new application
3. Copy your **Client ID** and **Client Secret**
4. Add your redirect URI to the app settings (e.g., `http://localhost:8888/api/v0/spotify/callback`)
5. Make sure to request the `user-library-read` scope to access saved albums

### Discogs API Setup

1. Go to [Discogs Developer Settings](https://www.discogs.com/settings/developers)
2. Generate a **Personal Access Token**
3. Copy the token to your `.env` file as `DISCOGS_ACCESS_TOKEN`
4. This token allows the app to search for album prices in the Discogs marketplace

### Environment Variables

| Variable | Description | Required |
|----------|-------------|----------|
| `SPOTIFY_CLIENT_ID` | Your Spotify app client ID | Yes |
| `SPOTIFY_CLIENT_SECRET` | Your Spotify app client secret | Yes |
| `SPOTIFY_REDIRECT_URI` | OAuth callback URL | Yes |
| `SPOTIFY_STATE` | Random string for OAuth state verification | Yes |
| `SPOTIFY_SCOPE` | Spotify API scopes (e.g., `user-library-read`) | Yes |
| `DISCOGS_ACCESS_TOKEN` | Your Discogs personal access token | Yes |

## 🎮 Usage

### Running the Application

Start the development server:
```bash
make run
```

The API will be available at `http://localhost:8888`

### API Endpoints

#### Home Page
```
GET /api/v0/spotify/
```
Returns the home page. If authenticated, shows user's albums and prices. Otherwise, shows landing page.

#### Initiate Spotify Login
```
GET /api/v0/spotify/login
```
Redirects to Spotify's OAuth authorization page. Users will be asked to grant permissions to access their Spotify data.

#### OAuth Callback
```
GET /api/v0/spotify/callback?code={code}&state={state}
```
Handles the OAuth callback from Spotify. Exchanges the authorization code for an access token and sets secure cookies.

**Response**: Returns success page and sets httponly cookies for session management.

#### Get User's Saved Albums
```
GET /api/v0/spotify/user_albums?limit={limit}
```
Retrieves the authenticated user's saved albums from Spotify.

**Parameters**:
- `limit` (int): Number of albums to fetch. Use `-1` to fetch all albums with pagination.

**Response**: JSON array of album objects with metadata (name, artist, release date, artwork, etc.)

#### Calculate Album Prices
```
POST /api/v0/spotify/get_albums_price
```
Calculates the cost of purchasing albums physically based on Discogs marketplace data.

**Request Body**:
```json
{
  "albums": [
    {
      "artist": "Artist Name",
      "album_name": "Album Title"
    }
  ]
}
```

**Response**:
```json
{
  "albums_with_price": [
    {
      "artist": "Artist Name",
      "album_name": "Album Title",
      "price": 12.50,
      "valid": true
    }
  ],
  "total": 12.50,
  "currency": "EUR"
}
```

### Example Flow

1. Start the server: `make run`
2. Navigate to: `http://localhost:8888/api/v0/spotify/`
3. Click the login button to authorize with Spotify
4. Grant permissions to access your library
5. Get redirected to the home page showing your albums
6. View your album collection with images and calculated CD prices
7. See the total cost of your collection in EUR

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

### Phase 1: Data Collection ✅ Completed
- [x] Spotify OAuth authentication
- [x] Fetch user's saved albums
- [x] Retrieve album metadata (artist, album, year, artwork)
- [x] Handle pagination for large collections

### Phase 2: Cost Calculation Engine ✅ Completed
- [x] Define physical format types (CD implemented, Vinyl/Cassette planned)
- [x] Integrate Discogs API for pricing data
- [x] Calculate costs per album based on marketplace data
- [x] Aggregate total collection cost
- [x] Intelligent price selection based on condition quality
- [ ] Handle special cases (compilations, box sets)

### Phase 3: User Experience ✅ In Progress
- [x] Web frontend for results visualization
- [x] Display albums with artwork and metadata
- [x] Breakdown by individual album with prices
- [x] Total cost calculation and display
- [x] Responsive design for mobile and desktop
- [ ] Breakdown by format type (CD/Vinyl/Cassette selector)
- [ ] Breakdown by artist/genre statistics
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
├── main.py                      # Application entry point
├── router.py                    # API routes
├── pyproject.toml              # Project metadata and dependencies
├── Makefile                    # Development commands
├── .env                        # Environment variables (not in repo)
├── .gitignore                  # Git ignore rules
├── README.md                   # This file
├── gateways/                   # External API integrations
│   ├── spotify_gateway.py      # Spotify API client and OAuth
│   ├── discogs_gateway.py      # Discogs API client and pricing
│   └── app_values.py           # Shared data models
├── values/                     # Pydantic models and settings
│   ├── spotify_values.py       # Spotify data models
│   └── discogs_values.py       # Discogs data models
└── static/                     # Frontend templates
    ├── index.html              # Landing page
    ├── home.html               # Authenticated user home page
    ├── error.html              # Error page
    └── spotify_oauth_success.html  # OAuth success page
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
