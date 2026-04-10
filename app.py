import dash
from dash import html, dcc
from dash.dependencies import Input, Output, State

from modules.youtube_search import search_youtube
from modules.database import save_search, get_history
from modules.voice_search import voice_to_text

app = dash.Dash(__name__)

# ---------------- UI ----------------
app.layout = html.Div([

    html.H1("FocusTube"),

    dcc.Input(
        id="search-box",
        type="text",
        placeholder="Search YouTube...",
        style={"width": "300px", "padding": "10px"}
    ),

    html.Button("Search", id="search-btn"),
    html.Button("Voice Search", id="voice-btn", style={"margin-left": "10px"}),

    dcc.Loading(
        id="loading",
        type="default",
        children=html.Div(id="results")
    ),

    html.Div(id="history")

])


# ---------------- CALLBACK ----------------
@app.callback(
    Output("results", "children"),
    Input("search-btn", "n_clicks"),
    Input("voice-btn", "n_clicks"),
    State("search-box", "value")
)
def update(search_clicks, voice_clicks, query):

    ctx = dash.callback_context

    if not ctx.triggered:
        return ""

    button_id = ctx.triggered[0]["prop_id"].split(".")[0]

    # 🎤 Voice search logic
    if button_id == "voice-btn":
        query = voice_to_text()

    if not query:
        return "No input detected"

    # 💾 Save search
    save_search(query)

    # 🔎 YouTube search
    videos = search_youtube(query)

    print(videos)

    cards = []

    for v in videos:

        cards.append(
            html.Div([

                html.Img(
                    src=v["thumbnail"],
                    style={"width": "100%", "border-radius": "10px"}
                ),

                html.P(v["title"]),

                html.A(
                    "Watch Video",
                    href=f"https://www.youtube.com/watch?v={v['video_id']}",
                    target="_blank"
                )

            ],
            style={
                "width": "280px",
                "margin": "12px",
                "padding": "10px",
                "background-color": "#181818",
                "border-radius": "12px",
                "box-shadow": "0px 2px 10px rgba(0,0,0,0.5)",
                "color": "white"
            })
        )

    # 📊 History
    history = get_history()

    history_ui = html.Div([
        html.H3("Recent Searches"),
        html.Ul([html.Li(h[0]) for h in history])
    ])

    return html.Div([
        history_ui,
        html.Div(cards, style={
            "display": "flex",
            "flex-wrap": "wrap",
            "justify-content": "center"
        })
    ])


# ---------------- RUN ----------------
if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port=8050)