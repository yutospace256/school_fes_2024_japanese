from flask import Flask, render_template, request, redirect, url_for, session 

@app.route('/')
def index():
    return render_template('index.html')