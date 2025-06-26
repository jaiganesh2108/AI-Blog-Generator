from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse
from django.conf import settings
import json
from pytube import YouTube
import os
import assemblyai as aai
import google.generativeai as genai
from pytube.exceptions import VideoUnavailable, RegexMatchError


# Homepage view (requires login)
@login_required
def index(request):
    return render(request, 'index.html')

# API endpoint to generate blog from YouTube link
@csrf_exempt
def generate_blog(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            yt_link = data['link']
        except (KeyError, json.JSONDecodeError):
            return JsonResponse({'error': 'Invalid data sent'}, status=400)
        
        # Get video title
        title = yt_title(yt_link)
        if not title:
            return JsonResponse({'error': 'Invalid or unavailable YouTube link'}, status=400)

        # Get transcript using AssemblyAI
        transcription = get_transcription(yt_link)
        if not transcription:
            return JsonResponse({'error': "Failed to get transcript"}, status=500)

        # Generate blog using Gemini
        blog_content = generate_blog_from_transcription(transcription)
        if not blog_content:
            return JsonResponse({'error': "Failed to generate blog article"}, status=500)

        # Return the blog content
        return JsonResponse({'content': blog_content})

    return JsonResponse({'error': 'Invalid request method'}, status=405)

# Helper: Get YouTube video title
def yt_title(link):
    try:
        yt = YouTube(link)
        return yt.title
    except (VideoUnavailable, RegexMatchError) as e:
        print(f"Invalid YouTube link or video unavailable: {e}")
        return None
    except Exception as e:
        print(f"Unexpected error getting title: {e}")
        return None

# Helper: Download audio from YouTube
def download_audio(link):
    yt = YouTube(link)
    video = yt.streams.filter(only_audio=True).first()
    out_file = video.download(output_path=settings.MEDIA_ROOT)
    base, ext = os.path.splitext(out_file)
    new_file = base + '.mp3'
    os.rename(out_file, new_file)
    return new_file

# Helper: Transcribe audio using AssemblyAI
def get_transcription(link):
    try:
        audio_file = download_audio(link)
        aai.settings.api_key = "e1b8186bdeee4e099bbcceb674784dc1"
        transcriber = aai.Transcriber()
        transcript = transcriber.transcribe(audio_file)
        return transcript.text
    except Exception as e:
        print(f"Transcription error: {e}")
        return None

# Helper: Generate blog article using Gemini
def generate_blog_from_transcription(transcription):
    try:
        genai.configure(api_key="AIzaSyCTzEaMVhN27q9ZytEVNAJzHGi8OXhW2oo")
        model = genai.GenerativeModel("gemini-pro")

        prompt = f"""
        Based on the following transcript from a YouTube video, write a comprehensive blog article.
        Do not make it sound like a video transcript. Format it like a formal, well-written blog post.

        Transcript:
        {transcription}

        Blog Article:
        """
        response = model.generate_content(prompt)
        return response.text.strip()
    except Exception as e:
        print(f"Gemini API error: {e}")
        return None

# Login view
def user_login(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']

        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('/')
        else:
            return render(request, 'login.html', {'error_message': "Invalid username or password"})
    return render(request, 'login.html')

# Signup view
def user_signup(request):
    if request.method == 'POST':
        username = request.POST['username']
        email = request.POST['email']
        password = request.POST['password']
        repeat_password = request.POST['repeatPassword']

        if password == repeat_password:
            try:
                user = User.objects.create_user(username, email, password)
                user.save()
                login(request, user)
                return redirect('/')
            except:
                return render(request, 'signup.html', {'error_message': 'Error creating account'})
        else:
            return render(request, 'signup.html', {'error_message': 'Passwords do not match!'})
    return render(request, 'signup.html')

# Logout view
def user_logout(request):
    logout(request)
    return redirect('/')
