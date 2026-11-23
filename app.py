"""Local-only Flask dashboard for synthetic Vling/YouTube-style records."""
import os
from contextlib import closing
from flask import Flask,abort,jsonify,redirect,render_template,request,url_for
from pipeline import connect,list_channels,list_videos,annotate,stats

def create_app(db_path=None):
    app=Flask(__name__)
    app.config["DATABASE"]=str(db_path or os.getenv("DEMO_DB_PATH","synthetic_warehouse.sqlite"))

    @app.get("/")
    def dashboard():
        with closing(connect(app.config["DATABASE"])) as db:
            return render_template("channels.html",items=list_channels(db),stats=stats(db))

    @app.get("/videos")
    def video_page():
        with closing(connect(app.config["DATABASE"])) as db:
            return render_template("videos.html",items=list_videos(db),stats=stats(db))

    @app.get("/api/summary")
    def summary_api():
        with closing(connect(app.config["DATABASE"])) as db:
            return jsonify(stats(db))

    @app.get("/api/channels")
    def channels_api():
        with closing(connect(app.config["DATABASE"])) as db:
            return jsonify(list_channels(db))

    @app.get("/api/videos")
    def videos_api():
        with closing(connect(app.config["DATABASE"])) as db:
            return jsonify(list_videos(db))

    @app.post("/note/<kind>/<code>")
    def note(kind,code):
        if kind not in ("channel","video"):
            abort(404)
        with closing(connect(app.config["DATABASE"])) as db:
            try:
                updated=annotate(db,kind,code,request.form.get("note",""))
            except ValueError:
                abort(400)
            if not updated:
                abort(404)
        return redirect(url_for("dashboard" if kind=="channel" else "video_page"))

    @app.after_request
    def no_cache(response):
        response.headers["Cache-Control"]="no-store"
        return response

    return app

if __name__=="__main__":
    create_app().run(host="127.0.0.1",port=5000,debug=False)
