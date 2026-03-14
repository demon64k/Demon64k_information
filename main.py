from fastapi import FastAPI
from fastapi.responses import HTMLResponse
import uvicorn
import os

app = FastAPI()

HTML_CONTENT = """
<!DOCTYPE html>
<html lang="ru">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Demon64k Information Bot</title>
    <link href="https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700;800;900&display=swap" rel="stylesheet">
    <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.4.0/css/all.min.css">
    <style>
        /* === БАЗОВЫЕ СТИЛИ === */
        * { margin: 0; padding: 0; box-sizing: border-box; }

        :root {
            --primary: #ff3b3b;
            --primary-light: #ff6b6b;
            --primary-dark: #d32f2f;
            --bg-dark: #0a0a0a;
            --bg-card: #1a1a1a;
            --bg-light: #141414;
            --text-main: #e0e0e0;
            --text-muted: #a0a0a0;
            --text-light: #ffffff;
            --border: rgba(255, 59, 59, 0.2);
            --shadow: rgba(255, 59, 59, 0.3);
        }

        body {
            background: linear-gradient(135deg, #0a0a0a 0%, #1a1a2e 50%, #0f0f0f 100%);
            color: var(--text-main);
            font-family: 'Inter', -apple-system, BlinkMacSystemFont, 'Segoe UI', sans-serif;
            line-height: 1.6;
            min-height: 100vh;
            overflow-x: hidden;
        }

        a { text-decoration: none; color: inherit; transition: all 0.3s ease; }
        ul { list-style: none; }

        .container { max-width: 1200px; margin: 0 auto; padding: 0 20px; }

        /* === ФОНОВЫЕ ЭФФЕКТЫ === */
        .bg-effects {
            position: fixed;
            top: 0; left: 0;
            width: 100%; height: 100%;
            z-index: -1;
            overflow: hidden;
            pointer-events: none;
        }

        /* Матрица */
        .matrix-canvas {
            position: absolute;
            top: 0; left: 0;
            width: 100%; height: 100%;
            opacity: 0.15;
        }

        /* Огонь */
        .fire-container {
            position: absolute;
            bottom: 0;
            left: 0;
            width: 100%;
            height: 100%;
            pointer-events: none;
        }

        .fire-particle {
            position: absolute;
            bottom: -10px;
            width: 4px;
            height: 4px;
            background: radial-gradient(circle, #ff6b35 0%, #ff3b3b 50%, transparent 100%);
            border-radius: 50%;
            animation: fireRise 4s infinite ease-in;
            opacity: 0;
            box-shadow: 0 0 10px #ff3b3b, 0 0 20px #ff6b35;
        }

        @keyframes fireRise {
            0% {
                opacity: 0;
                transform: translateY(0) scale(1);
            }
            10% {
                opacity: 0.8;
            }
            50% {
                opacity: 0.6;
            }
            100% {
                opacity: 0;
                transform: translateY(-100vh) scale(0.5);
            }
        }

        .fire-particle:nth-child(odd) {
            animation-duration: 3s;
            animation-delay: 0s;
        }

        .fire-particle:nth-child(even) {
            animation-duration: 5s;
            animation-delay: 1s;
        }

        /* Плавающие круги */
        .bg-animation {
            position: absolute;
            top: 0; left: 0;
            width: 100%; height: 100%;
        }

        .bg-animation .circle {
            position: absolute;
            border-radius: 50%;
            background: radial-gradient(circle, rgba(255,59,59,0.2) 0%, transparent 70%);
            animation: float 20s infinite ease-in-out;
            opacity: 0.3;
        }

        .bg-animation .circle:nth-child(1) {
            width: 400px; height: 400px;
            top: -200px; left: -200px;
            animation-delay: 0s;
        }

        .bg-animation .circle:nth-child(2) {
            width: 300px; height: 300px;
            top: 50%; right: -150px;
            animation-delay: 5s;
        }

        .bg-animation .circle:nth-child(3) {
            width: 250px; height: 250px;
            bottom: -125px; left: 30%;
            animation-delay: 10s;
        }

        @keyframes float {
            0%, 100% { transform: translate(0, 0) scale(1); }
            25% { transform: translate(30px, -30px) scale(1.1); }
            50% { transform: translate(-20px, 20px) scale(0.9); }
            75% { transform: translate(20px, 30px) scale(1.05); }
        }

        /* Искры */
        .ember {
            position: absolute;
            width: 3px;
            height: 3px;
            background: radial-gradient(circle, #ffcc00 0%, #ff6b35 50%, transparent 100%);
            border-radius: 50%;
            animation: emberFloat 6s infinite ease-in-out;
            opacity: 0;
            box-shadow: 0 0 8px #ff6b35;
        }

        @keyframes emberFloat {
            0% {
                opacity: 0;
                transform: translateY(100vh) rotate(0deg);
            }
            10% {
                opacity: 0.8;
            }
            50% {
                opacity: 0.5;
                transform: translateY(50vh) rotate(180deg);
            }
            90% {
                opacity: 0.3;
            }
            100% {
                opacity: 0;
                transform: translateY(-100px) rotate(360deg);
            }
        }

        /* === ШАПКА === */
        header {
            padding: 20px 0;
            position: fixed;
            top: 0; left: 0; right: 0;
            z-index: 1000;
            background: rgba(15, 15, 15, 0.9);
            backdrop-filter: blur(20px);
            border-bottom: 1px solid var(--border);
            animation: slideDown 0.8s ease-out;
        }

        @keyframes slideDown {
            from { transform: translateY(-100%); opacity: 0; }
            to { transform: translateY(0); opacity: 1; }
        }

        .nav-content {
            display: flex;
            justify-content: space-between;
            align-items: center;
        }

        .logo {
            font-size: 1.8rem;
            font-weight: 900;
            background: linear-gradient(135deg, #ff3b3b 0%, #ff6b6b 100%);
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
            background-clip: text;
            text-transform: uppercase;
            letter-spacing: 3px;
            display: flex;
            align-items: center;
            gap: 10px;
            animation: glow 3s ease-in-out infinite;
        }

        .logo i {
            font-size: 2rem;
            background: linear-gradient(135deg, #ff3b3b, #ff6b6b);
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
            filter: drop-shadow(0 0 10px rgba(255, 59, 59, 0.6));
            animation: iconPulse 2s ease-in-out infinite;
        }

        @keyframes glow {
            0%, 100% { filter: drop-shadow(0 0 5px rgba(255, 59, 59, 0.4)); }
            50% { filter: drop-shadow(0 0 15px rgba(255, 59, 59, 0.7)); }
        }

        @keyframes iconPulse {
            0%, 100% { transform: scale(1) rotate(0deg); }
            50% { transform: scale(1.1) rotate(5deg); }
        }

        .nav-links {
            display: flex;
            gap: 15px;
            align-items: center;
        }

        .btn {
            display: inline-flex;
            align-items: center;
            gap: 8px;
            padding: 10px 22px;
            border-radius: 25px;
            font-weight: 600;
            font-size: 0.95rem;
            transition: all 0.35s cubic-bezier(0.4, 0, 0.2, 1);
            position: relative;
            overflow: hidden;
            cursor: pointer;
            border: 2px solid transparent;
        }

        .btn i {
            font-size: 1rem;
            transition: transform 0.3s ease;
        }

        .btn:hover i {
            transform: translateX(3px) rotate(360deg) scale(1.2);
        }

        .btn::before {
            content: '';
            position: absolute;
            top: 0; left: -100%;
            width: 100%; height: 100%;
            background: linear-gradient(90deg, transparent, rgba(255,255,255,0.2), transparent);
            transition: left 0.5s ease;
            z-index: 0;
        }

        .btn:hover::before {
            left: 100%;
        }

        .btn > * {
            position: relative;
            z-index: 1;
        }

        .btn-primary {
            background: linear-gradient(135deg, #ff3b3b, #ff6b6b);
            color: white;
            box-shadow: 0 5px 20px rgba(255, 59, 59, 0.4);
        }

        .btn-primary:hover {
            transform: translateY(-3px);
            box-shadow: 0 10px 35px rgba(255, 59, 59, 0.6);
        }

        .btn-outline {
            background: transparent;
            color: #ff3b3b;
            border-color: #ff3b3b;
        }

        .btn-outline:hover {
            background: #ff3b3b;
            color: white;
            transform: translateY(-3px);
            box-shadow: 0 10px 35px rgba(255, 59, 59, 0.4);
        }

        /* === ГЛАВНЫЙ ЭКРАН === */
        .hero {
            padding: 180px 0 120px;
            text-align: center;
            position: relative;
        }

        .hero-badge {
            display: inline-flex;
            align-items: center;
            gap: 10px;
            background: rgba(255, 59, 59, 0.15);
            border: 1px solid rgba(255, 59, 59, 0.3);
            padding: 9px 20px;
            border-radius: 20px;
            color: #ff6b6b;
            font-size: 0.9rem;
            margin-bottom: 25px;
            animation: fadeInUp 0.8s ease-out;
        }

        .hero-badge i {
            animation: badgeSpin 3s linear infinite;
        }

        @keyframes badgeSpin {
            0% { transform: rotate(0deg); }
            100% { transform: rotate(360deg); }
        }

        .hero h1 {
            font-size: 4rem;
            font-weight: 900;
            margin-bottom: 25px;
            background: linear-gradient(135deg, #ffffff 0%, #ff3b3b 50%, #ff6b6b 100%);
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
            background-clip: text;
            animation: titlePulse 3s ease-in-out infinite;
            line-height: 1.2;
        }

        @keyframes titlePulse {
            0%, 100% { transform: scale(1); }
            50% { transform: scale(1.02); }
        }

        .hero p {
            font-size: 1.3rem;
            color: var(--text-muted);
            max-width: 700px;
            margin: 0 auto 50px;
            animation: fadeInUp 1s ease-out 0.3s both;
        }

        @keyframes fadeInUp {
            from { opacity: 0; transform: translateY(30px); }
            to { opacity: 1; transform: translateY(0); }
        }

        .btn-main {
            display: inline-flex;
            align-items: center;
            gap: 12px;
            background: linear-gradient(135deg, #ff3b3b 0%, #ff6b6b 100%);
            color: white;
            padding: 18px 50px;
            font-size: 1.3rem;
            font-weight: 700;
            border-radius: 50px;
            border: none;
            cursor: pointer;
            box-shadow: 0 10px 30px rgba(255, 59, 59, 0.4);
            transition: all 0.4s cubic-bezier(0.4, 0, 0.2, 1);
            position: relative;
            overflow: hidden;
            animation: fadeInUp 1s ease-out 0.6s both, buttonFloat 3s ease-in-out infinite;
        }

        @keyframes buttonFloat {
            0%, 100% { transform: translateY(0); }
            50% { transform: translateY(-10px); }
        }

        .btn-main i {
            font-size: 1.3rem;
            transition: transform 0.3s ease;
        }

        .btn-main:hover i {
            transform: translateY(-3px) rotate(-10deg) scale(1.2);
        }

        .btn-main::before {
            content: '';
            position: absolute;
            top: 50%; left: 50%;
            width: 0; height: 0;
            border-radius: 50%;
            background: rgba(255, 255, 255, 0.3);
            transform: translate(-50%, -50%);
            transition: width 0.6s ease, height 0.6s ease;
            z-index: 0;
        }

        .btn-main:hover::before {
            width: 350px; height: 350px;
        }

        .btn-main:hover {
            transform: translateY(-5px) scale(1.05);
            box-shadow: 0 15px 40px rgba(255, 59, 59, 0.6);
        }

        .btn-main > * {
            position: relative;
            z-index: 1;
        }

        /* === СЕКЦИИ === */
        .section {
            padding: 100px 0;
            position: relative;
        }

        .section-dark {
            background: rgba(20, 20, 20, 0.7);
        }

        .section-title {
            text-align: center;
            font-size: 3rem;
            font-weight: 800;
            margin-bottom: 20px;
            background: linear-gradient(135deg, #ffffff 0%, #ff3b3b 100%);
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
            background-clip: text;
            animation: fadeInUp 1s ease-out;
        }

        .section-subtitle {
            text-align: center;
            color: var(--text-muted);
            font-size: 1.1rem;
            margin-bottom: 60px;
            animation: fadeInUp 1s ease-out 0.2s both;
        }

        /* === КАРТОЧКИ === */
        .grid {
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(300px, 1fr));
            gap: 35px;
        }

        .card {
            background: rgba(26, 26, 26, 0.8);
            padding: 45px 35px;
            border-radius: 25px;
            border: 1px solid rgba(255, 59, 59, 0.15);
            transition: all 0.4s cubic-bezier(0.175, 0.885, 0.32, 1.275);
            position: relative;
            overflow: hidden;
            backdrop-filter: blur(10px);
            animation: fadeInUp 1s ease-out both;
            text-align: center;
        }

        .card:nth-child(1) { animation-delay: 0.1s; }
        .card:nth-child(2) { animation-delay: 0.2s; }
        .card:nth-child(3) { animation-delay: 0.3s; }
        .card:nth-child(4) { animation-delay: 0.4s; }

        .card::before {
            content: '';
            position: absolute;
            top: 0; left: -100%;
            width: 100%; height: 100%;
            background: linear-gradient(90deg, transparent, rgba(255, 59, 59, 0.1), transparent);
            transition: left 0.7s ease;
        }

        .card:hover::before {
            left: 100%;
        }

        .card:hover {
            border-color: #ff3b3b;
            transform: translateY(-15px) scale(1.03);
            box-shadow: 0 25px 50px rgba(255, 59, 59, 0.3);
        }

        .card-icon {
            font-size: 4rem;
            margin-bottom: 25px;
            display: inline-block;
            animation: iconBounce 2s ease-in-out infinite;
            background: linear-gradient(135deg, #ff3b3b, #ff6b6b);
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
            filter: drop-shadow(0 0 15px rgba(255, 59, 59, 0.5));
        }

        @keyframes iconBounce {
            0%, 100% { transform: translateY(0) rotate(0deg); }
            25% { transform: translateY(-10px) rotate(-5deg); }
            75% { transform: translateY(-5px) rotate(5deg); }
        }

        .card h3 {
            color: #ff3b3b;
            margin-bottom: 15px;
            font-size: 1.7rem;
            font-weight: 700;
        }

        .card p {
            color: var(--text-muted);
            font-size: 1rem;
            line-height: 1.7;
        }

        /* === СОЗДАТЕЛЬ === */
        .creator-section {
            padding: 100px 0;
            background: rgba(15, 15, 15, 0.85);
        }

        .creator-card {
            max-width: 800px;
            margin: 0 auto;
            background: linear-gradient(135deg, rgba(255, 59, 59, 0.1), rgba(26, 26, 26, 0.85));
            border: 2px solid rgba(255, 59, 59, 0.3);
            border-radius: 30px;
            padding: 60px 40px;
            text-align: center;
            backdrop-filter: blur(20px);
            animation: fadeInUp 1s ease-out;
            box-shadow: 0 20px 60px rgba(255, 59, 59, 0.2);
        }

        .creator-avatar-frame {
            position: relative;
            width: 150px;
            height: 150px;
            margin: 0 auto 30px;
            border-radius: 50%;
            padding: 5px;
            background: linear-gradient(135deg, #ff3b3b, #ff6b6b);
            box-shadow: 0 10px 50px rgba(255, 59, 59, 0.5);
            animation: avatarPulse 3s ease-in-out infinite;
        }

        .creator-avatar-window {
            width: 100%;
            height: 100%;
            border-radius: 50%;
            background: linear-gradient(135deg, #1a1a2e, #0f0f0f);
            display: flex;
            align-items: center;
            justify-content: center;
            overflow: hidden;
            position: relative;
            border: 3px solid rgba(255, 255, 255, 0.1);
        }

        .creator-avatar-window img {
            width: 100%;
            height: 100%;
            object-fit: cover;
            border-radius: 50%;
            transition: transform 0.4s ease;
        }

        .creator-avatar-window:hover img {
            transform: scale(1.1);
        }

        @keyframes avatarPulse {
            0%, 100% { transform: scale(1); box-shadow: 0 10px 50px rgba(255, 59, 59, 0.5); }
            50% { transform: scale(1.05); box-shadow: 0 15px 60px rgba(255, 59, 59, 0.7); }
        }

        .creator-card h2 {
            font-size: 2.5rem;
            margin-bottom: 15px;
            background: linear-gradient(135deg, #ffffff, #ff3b3b);
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
            background-clip: text;
        }

        .creator-card .username {
            color: #ff6b6b;
            font-size: 1.3rem;
            margin-bottom: 25px;
            font-weight: 600;
        }

        .creator-card p {
            color: var(--text-muted);
            font-size: 1.1rem;
            line-height: 1.8;
            margin-bottom: 30px;
        }

        .creator-links {
            display: flex;
            gap: 15px;
            justify-content: center;
            flex-wrap: wrap;
            margin-bottom: 20px;
        }

        .btn-creator {
            display: inline-flex;
            align-items: center;
            gap: 10px;
            padding: 14px 35px;
            border-radius: 30px;
            font-weight: 600;
            transition: all 0.35s cubic-bezier(0.4, 0, 0.2, 1);
            position: relative;
            overflow: hidden;
        }

        .btn-creator i {
            transition: transform 0.3s ease;
        }

        .btn-creator:hover i {
            transform: translateY(-3px) scale(1.2);
        }

        .btn-creator::before {
            content: '';
            position: absolute;
            top: 0; left: -100%;
            width: 100%; height: 100%;
            background: linear-gradient(90deg, transparent, rgba(255,255,255,0.2), transparent);
            transition: left 0.5s ease;
        }

        .btn-creator:hover::before {
            left: 100%;
        }

        .btn-creator-telegram {
            background: linear-gradient(135deg, #0088cc, #00a8e8);
            color: white;
            box-shadow: 0 5px 20px rgba(0, 136, 204, 0.4);
        }

        .btn-creator-telegram:hover {
            transform: translateY(-5px);
            box-shadow: 0 10px 35px rgba(0, 136, 204, 0.6);
        }

        .btn-creator-channel {
            background: rgba(255, 59, 59, 0.15);
            border: 2px solid rgba(255, 59, 59, 0.3);
            color: #ff3b3b;
        }

        .btn-creator-channel:hover {
            background: rgba(255, 59, 59, 0.25);
            border-color: #ff3b3b;
            transform: translateY(-5px);
            box-shadow: 0 10px 30px rgba(255, 59, 59, 0.3);
        }

        .creator-social {
            display: flex;
            gap: 14px;
            justify-content: center;
            margin-top: 18px;
        }

        .social-icon {
            width: 50px;
            height: 50px;
            border-radius: 14px;
            display: flex;
            align-items: center;
            justify-content: center;
            font-size: 1.4rem;
            transition: all 0.35s cubic-bezier(0.4, 0, 0.2, 1);
            position: relative;
            overflow: hidden;
            border: 1px solid transparent;
        }

        .social-icon i {
            position: relative;
            z-index: 1;
            transition: transform 0.3s ease;
        }

        .social-icon:hover i {
            transform: scale(1.15);
        }

        .social-icon::before {
            content: '';
            position: absolute;
            top: 0; left: -100%;
            width: 100%; height: 100%;
            background: linear-gradient(90deg, transparent, rgba(255,255,255,0.25), transparent);
            transition: left 0.5s ease;
            z-index: 0;
        }

        .social-icon:hover::before {
            left: 100%;
        }

        .social-icon.github {
            background: linear-gradient(135deg, rgba(45, 50, 58, 0.5), rgba(65, 75, 88, 0.4));
            color: #c9d1d9;
            border-color: rgba(201, 209, 217, 0.3);
        }

        .social-icon.github:hover {
            background: linear-gradient(135deg, rgba(45, 50, 58, 0.7), rgba(65, 75, 88, 0.5));
            color: #ffffff;
            border-color: rgba(201, 209, 217, 0.6);
            transform: translateY(-5px);
            box-shadow: 0 10px 28px rgba(36, 41, 46, 0.5);
        }

        .social-icon.pinterest {
            background: linear-gradient(135deg, rgba(230, 0, 35, 0.3), rgba(255, 40, 75, 0.25));
            color: #ffc4d4;
            border-color: rgba(255, 164, 184, 0.35);
        }

        .social-icon.pinterest:hover {
            background: linear-gradient(135deg, rgba(230, 0, 35, 0.5), rgba(255, 40, 75, 0.35));
            color: #ffffff;
            border-color: rgba(255, 164, 184, 0.6);
            transform: translateY(-5px);
            box-shadow: 0 10px 28px rgba(230, 0, 35, 0.4);
        }

        /* === КАНАЛ === */
        .channel-section {
            padding: 100px 0;
            background: linear-gradient(135deg, rgba(255, 59, 59, 0.1), rgba(26, 26, 46, 0.85));
            text-align: center;
            position: relative;
            overflow: hidden;
        }

        .channel-section::before {
            content: '';
            position: absolute;
            top: -50%; left: -50%;
            width: 200%; height: 200%;
            background: radial-gradient(circle, rgba(255, 59, 59, 0.1) 0%, transparent 70%);
            animation: rotate 30s linear infinite;
        }

        @keyframes rotate {
            0% { transform: rotate(0deg); }
            100% { transform: rotate(360deg); }
        }

        .channel-content {
            position: relative;
            z-index: 1;
        }

        .channel-section h2 {
            font-size: 2.5rem;
            margin-bottom: 20px;
            color: #ffffff;
            animation: fadeInUp 1s ease-out;
            display: flex;
            align-items: center;
            justify-content: center;
            gap: 15px;
        }

        .channel-section h2 i {
            font-size: 2.8rem;
            animation: megaphoneWave 2s ease-in-out infinite;
            background: linear-gradient(135deg, #0088cc, #00a8e8);
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
        }

        @keyframes megaphoneWave {
            0%, 100% { transform: rotate(-10deg) scale(1); }
            50% { transform: rotate(10deg) scale(1.1); }
        }

        .channel-section p {
            color: var(--text-muted);
            font-size: 1.2rem;
            margin-bottom: 40px;
            max-width: 600px;
            margin-left: auto;
            margin-right: auto;
            animation: fadeInUp 1s ease-out 0.2s both;
        }

        .btn-channel {
            display: inline-flex;
            align-items: center;
            gap: 12px;
            background: linear-gradient(135deg, #0088cc 0%, #00a8e8 100%);
            color: white;
            padding: 18px 45px;
            border-radius: 50px;
            font-size: 1.2rem;
            font-weight: 700;
            box-shadow: 0 10px 30px rgba(0, 136, 204, 0.4);
            transition: all 0.4s cubic-bezier(0.4, 0, 0.2, 1);
            position: relative;
            overflow: hidden;
            animation: fadeInUp 1s ease-out 0.4s both, buttonFloat 3s ease-in-out infinite;
        }

        .btn-channel::before {
            content: '';
            position: absolute;
            top: 50%; left: 50%;
            width: 0; height: 0;
            border-radius: 50%;
            background: rgba(255, 255, 255, 0.3);
            transform: translate(-50%, -50%);
            transition: width 0.6s ease, height 0.6s ease;
            z-index: 0;
        }

        .btn-channel:hover::before {
            width: 320px; height: 320px;
        }

        .btn-channel i {
            font-size: 1.5rem;
            transition: transform 0.3s ease;
        }

        .btn-channel:hover i {
            transform: translateY(-3px) rotate(-10deg) scale(1.2);
        }

        .btn-channel:hover {
            transform: translateY(-5px) scale(1.05);
            box-shadow: 0 15px 40px rgba(0, 136, 204, 0.6);
        }

        .btn-channel > * {
            position: relative;
            z-index: 1;
        }

        /* === ПОДВАЛ === */
        footer {
            padding: 60px 0 30px;
            text-align: center;
            border-top: 1px solid rgba(255, 59, 59, 0.15);
            background: rgba(10, 10, 10, 0.95);
            position: relative;
        }

        .footer-content {
            position: relative;
            z-index: 1;
        }

        .social-links {
            margin-bottom: 30px;
            display: flex;
            justify-content: center;
            gap: 20px;
        }

        .social-links a {
            width: 56px;
            height: 56px;
            background: rgba(255, 59, 59, 0.12);
            border: 2px solid rgba(255, 59, 59, 0.3);
            border-radius: 50%;
            display: flex;
            align-items: center;
            justify-content: center;
            font-size: 1.4rem;
            color: #ff3b3b;
            transition: all 0.35s cubic-bezier(0.4, 0, 0.2, 1);
            position: relative;
            overflow: hidden;
        }

        .social-links a i {
            transition: transform 0.3s ease;
            position: relative;
            z-index: 1;
        }

        .social-links a::before {
            content: '';
            position: absolute;
            top: 0; left: -100%;
            width: 100%; height: 100%;
            background: linear-gradient(90deg, transparent, rgba(255,255,255,0.2), transparent);
            transition: left 0.5s ease;
            z-index: 0;
        }

        .social-links a:hover::before {
            left: 100%;
        }

        .social-links a:hover {
            background: linear-gradient(135deg, #ff3b3b, #ff6b6b);
            color: white;
            transform: translateY(-8px) scale(1.15) rotate(360deg);
            box-shadow: 0 15px 30px rgba(255, 59, 59, 0.5);
            border-color: transparent;
        }

        .social-links a:hover i {
            transform: scale(1.1);
        }

        footer p {
            color: #666666;
            margin-bottom: 10px;
        }

        .creator-info {
            color: #888888;
            font-size: 0.95rem;
            margin-top: 20px;
        }

        .creator-info a {
            color: #ff3b3b;
            font-weight: 600;
            transition: all 0.3s ease;
        }

        .creator-info a:hover {
            color: #ff6b6b;
            text-decoration: underline;
        }

        /* === АНИМАЦИИ ПРИ СКРОЛЛЕ === */
        .scroll-reveal {
            opacity: 0;
            transform: translateY(50px);
            transition: all 0.8s ease-out;
        }

        .scroll-reveal.active {
            opacity: 1;
            transform: translateY(0);
        }

        /* === АДАПТИВНОСТЬ === */
        @media (max-width: 768px) {
            .hero h1 { font-size: 2.5rem; }
            .section-title { font-size: 2rem; }
            .nav-content { flex-direction: column; gap: 15px; }
            .hero { padding: 140px 0 80px; }
            .creator-card, .card { padding: 40px 25px; }
            .creator-card h2 { font-size: 2rem; }
            .grid { grid-template-columns: 1fr; }
            .creator-links { flex-direction: column; align-items: center; }
            .btn-creator { width: 100%; max-width: 300px; justify-content: center; }
            .btn-main { padding: 15px 40px; font-size: 1.1rem; }
            .creator-avatar-frame { width: 130px; height: 130px; }
        }

        /* === ЗАГРУЗКА === */
        .loader {
            position: fixed;
            top: 0; left: 0;
            width: 100%; height: 100%;
            background: #0a0a0a;
            display: flex;
            justify-content: center;
            align-items: center;
            z-index: 9999;
            transition: opacity 0.5s ease;
        }

        .loader.hidden {
            opacity: 0;
            pointer-events: none;
        }

        .loader-circle {
            width: 60px; height: 60px;
            border: 4px solid rgba(255, 59, 59, 0.15);
            border-top-color: #ff3b3b;
            border-radius: 50%;
            animation: spin 1s linear infinite;
            box-shadow: 0 0 20px rgba(255, 59, 59, 0.3);
        }

        @keyframes spin {
            to { transform: rotate(360deg); }
        }

        /* === УВЕДОМЛЕНИЕ О КОПИРОВАНИИ === */
        .copy-toast {
            position: fixed;
            bottom: 30px;
            left: 50%;
            transform: translateX(-50%) translateY(100px);
            background: linear-gradient(135deg, #ff3b3b, #ff6b6b);
            color: white;
            padding: 15px 30px;
            border-radius: 50px;
            font-weight: 600;
            font-size: 1rem;
            box-shadow: 0 10px 40px rgba(255, 59, 59, 0.5);
            display: flex;
            align-items: center;
            gap: 12px;
            z-index: 10000;
            opacity: 0;
            transition: all 0.4s cubic-bezier(0.175, 0.885, 0.32, 1.275);
            backdrop-filter: blur(10px);
            border: 2px solid rgba(255, 255, 255, 0.2);
            pointer-events: none;
        }

        .copy-toast.show {
            transform: translateX(-50%) translateY(0);
            opacity: 1;
        }

        .copy-toast i {
            font-size: 1.3rem;
            animation: toastIconBounce 0.6s ease-in-out;
        }

        @keyframes toastIconBounce {
            0% { transform: scale(0) rotate(-180deg); }
            50% { transform: scale(1.3) rotate(10deg); }
            100% { transform: scale(1) rotate(0deg); }
        }

        .copy-toast::before {
            content: '';
            position: absolute;
            top: 50%; left: 50%;
            width: 0; height: 0;
            border-radius: 50%;
            background: rgba(255, 255, 255, 0.3);
            transform: translate(-50%, -50%);
            transition: width 0.6s ease, height 0.6s ease;
            z-index: -1;
        }

        .copy-toast.show::before {
            width: 400px; height: 400px;
        }

        .copy-toast.hide {
            transform: translateX(-50%) translateY(-20px);
            opacity: 0;
        }

        /* === ВЫДЕЛЕНИЕ ТЕКСТА === */
        ::selection {
            background: rgba(255, 59, 59, 0.4);
            color: white;
        }

        ::-moz-selection {
            background: rgba(255, 59, 59, 0.4);
            color: white;
        }
    </style>
</head>
<body>
    <!-- Уведомление о копировании -->
    <div class="copy-toast" id="copyToast">
        <i class="fas fa-check-circle"></i>
        <span id="copyMessage">Скопировано!</span>
    </div>

    <!-- Загрузчик -->
    <div class="loader" id="loader">
        <div class="loader-circle"></div>
    </div>

    <!-- Фоновые эффекты -->
    <div class="bg-effects">
        <!-- Матрица -->
        <canvas class="matrix-canvas" id="matrixCanvas"></canvas>

        <!-- Огонь -->
        <div class="fire-container" id="fireContainer"></div>

        <!-- Плавающие круги -->
        <div class="bg-animation">
            <div class="circle"></div>
            <div class="circle"></div>
            <div class="circle"></div>
        </div>
    </div>

    <!-- Шапка -->
    <header>
        <div class="container nav-content">
            <div class="logo">
                <i class="fas fa-robot"></i>
                Demon64k Bot
            </div>
            <div class="nav-links">
                <a href="#features" class="btn btn-outline">
                    <i class="fas fa-star"></i> Возможности
                </a>
                <a href="https://t.me/Demon64k_information_bot" class="btn btn-primary">
                    <i class="fab fa-telegram-plane"></i> Запустить
                </a>
            </div>
        </div>
    </header>

    <!-- Главный экран -->
    <section class="hero">
        <div class="container">
            <div class="hero-badge">
                <i class="fas fa-search"></i>
                Поиск информации о пользователях
            </div>
            <h1>Demon64k ID Bot</h1>
            <p>
                Бот для поиска базовой информации о пользователях в Telegram: 
                ID, никнейм, язык, юзернейм. Быстро, удобно и бесплатно!
            </p>
            <a href="https://t.me/Demon64k_information_bot" class="btn-main">
                <i class="fab fa-telegram-plane"></i>
                Запустить бота
            </a>
        </div>
    </section>

    <!-- Зачем нужен ID -->
    <section class="section section-dark">
        <div class="container">
            <div class="card scroll-reveal" style="max-width: 900px; margin: 0 auto; padding: 60px 40px;">
                <h2 class="section-title">
                    <i class="fas fa-question-circle"></i>
                    Зачем нужен ID?
                </h2>
                <p style="color: var(--text-muted); font-size: 1.1rem; line-height: 1.8; margin-bottom: 40px; text-align: center;">
                    Для обычных пользователей он навряд ли понадобится, но вот для разработчиков телеграм-ботов он во многом может пригодиться:
                </p>
                <div class="grid">
                    <div class="card" style="padding: 30px 25px; animation-delay: 0.1s;">
                        <div class="card-icon"><i class="fas fa-code"></i></div>
                        <h3>Создание ботов</h3>
                        <p>Сделать похожий бот для своих проектов и задач</p>
                    </div>
                    <div class="card" style="padding: 30px 25px; animation-delay: 0.2s;">
                        <div class="card-icon"><i class="fas fa-bell"></i></div>
                        <h3>Уведомления</h3>
                        <p>Отправка уведомлений создателю о новых пользователях</p>
                    </div>
                    <div class="card" style="padding: 30px 25px; animation-delay: 0.3s;">
                        <div class="card-icon"><i class="fas fa-users"></i></div>
                        <h3>Идентификация</h3>
                        <p>Не путать пользователей с одинаковыми именами</p>
                    </div>
                    <div class="card" style="padding: 30px 25px; animation-delay: 0.4s;">
                        <div class="card-icon"><i class="fas fa-cogs"></i></div>
                        <h3>И другое</h3>
                        <p>Множество применений для разработки</p>
                    </div>
                </div>
            </div>
        </div>
    </section>

    <!-- Что показывает бот -->
    <section class="section">
        <div class="container">
            <h2 class="section-title scroll-reveal">Что показывает бот</h2>
            <p class="section-subtitle scroll-reveal">Полная информация о пользователе</p>
            <div class="grid">
                <div class="card scroll-reveal">
                    <div class="card-icon"><i class="fas fa-fingerprint"></i></div>
                    <h3>ID пользователя</h3>
                    <p>Уникальный идентификатор</p>
                </div>
                <div class="card scroll-reveal">
                    <div class="card-icon"><i class="fas fa-at"></i></div>
                    <h3>Юзернейм</h3>
                    <p>Имя пользователя @username</p>
                </div>
                <div class="card scroll-reveal">
                    <div class="card-icon"><i class="fas fa-user-tag"></i></div>
                    <h3>Никнейм</h3>
                    <p>Отображаемое имя</p>
                </div>
                <div class="card scroll-reveal">
                    <div class="card-icon"><i class="fas fa-language"></i></div>
                    <h3>Язык</h3>
                    <p>Язык интерфейса Telegram</p>
                </div>
            </div>
        </div>
    </section>

    <!-- Создатель -->
    <section class="creator-section">
        <div class="container">
            <div class="creator-card scroll-reveal">
                <div class="creator-avatar-frame">
                    <div class="creator-avatar-window">
                        <img src="https://i.pinimg.com/736x/45/de/dc/45dedceb94dae8daf85a056c8af16eb6.jpg" alt="Создатель">
                    </div>
                </div>
                <h2>Создатель бота</h2>
                <div class="username">Donald Trump</div>
                <p>
                    Разработчик и основатель Demon64k Information Bot. 
                    Создаю удобные и функциональные решения для Telegram. 
                    Всегда открыт к сотрудничеству и новым идеям!
                </p>

                <div class="creator-links">
                    <a href="https://t.me/Trump1238" target="_blank" class="btn-creator btn-creator-telegram">
                        <i class="fab fa-telegram-plane"></i>
                        Telegram
                    </a>
                    <a href="https://t.me/Demon64k_poisk" target="_blank" class="btn-creator btn-creator-channel">
                        <i class="fas fa-broadcast-tower"></i>
                        Канал
                    </a>
                </div>

                <div class="creator-social">
                    <a href="https://github.com/demon64k" target="_blank" class="social-icon github" title="GitHub">
                        <i class="fab fa-github"></i>
                    </a>
                    <a href="https://pin.it/6JRrwXT1O" target="_blank" class="social-icon pinterest" title="Pinterest">
                        <i class="fab fa-pinterest"></i>
                    </a>
                </div>
            </div>
        </div>
    </section>

    <!-- Преимущества -->
    <section class="section" id="features">
        <div class="container">
            <h2 class="section-title scroll-reveal">Преимущества</h2>
            <p class="section-subtitle scroll-reveal">Почему стоит использовать наш бот</p>
            <div class="grid">
                <div class="card scroll-reveal">
                    <div class="card-icon"><i class="fas fa-bolt"></i></div>
                    <h3>Быстрый ответ</h3>
                    <p>Мгновенное получение информации о пользователе без задержек</p>
                </div>
                <div class="card scroll-reveal">
                    <div class="card-icon"><i class="fas fa-shield-alt"></i></div>
                    <h3>Безопасность</h3>
                    <p>Бот не хранит личные данные и не передаёт их третьим лицам</p>
                </div>
                <div class="card scroll-reveal">
                    <div class="card-icon"><i class="fas fa-mobile-alt"></i></div>
                    <h3>Удобство</h3>
                    <p>Простое управление прямо в Telegram без лишних приложений</p>
                </div>
                <div class="card scroll-reveal">
                    <div class="card-icon"><i class="fas fa-gift"></i></div>
                    <h3>Бесплатно</h3>
                    <p>Полный доступ ко всем функциям бота без ограничений</p>
                </div>
            </div>
        </div>
    </section>

    <!-- Канал -->
    <section class="channel-section">
        <div class="container channel-content">
            <h2 class="scroll-reveal">
                <i class="fas fa-bullhorn"></i>
                Наш канал
            </h2>
            <p class="scroll-reveal">
                Подпишитесь на наш канал @Demon64k_poisk, чтобы быть в курсе всех обновлений и новостей
            </p>
            <a href="https://t.me/Demon64k_poisk" target="_blank" class="btn-channel scroll-reveal">
                <i class="fab fa-telegram-plane"></i>
                Подписаться на канал
            </a>
        </div>
    </section>

    <!-- Подвал -->
    <footer>
        <div class="container footer-content">
            <div class="social-links">
                <a href="https://t.me/Demon64k_information_bot" title="Запустить бота">
                    <i class="fab fa-telegram-plane"></i>
                </a>
                <a href="https://t.me/Demon64k_poisk" title="Наш канал">
                    <i class="fas fa-broadcast-tower"></i>
                </a>
                <a href="https://t.me/Trump1238" title="Создатель">
                    <i class="fas fa-user-shield"></i>
                </a>
                <a href="https://github.com/demon64k" target="_blank" title="GitHub">
                    <i class="fab fa-github"></i>
                </a>
                <a href="https://pin.it/6JRrwXT1O" target="_blank" title="Pinterest">
                    <i class="fab fa-pinterest"></i>
                </a>
            </div>
            <p>&copy; 2026 Demon64k Information Bot. Все права защищены.</p>
            <div class="creator-info">
                Создатель: <a href="https://t.me/Trump1238" target="_blank">@Trump1238</a>
            </div>
        </div>
    </footer>

    <!-- Скрипты -->
    <script>
        // Скрыть загрузчик
        window.addEventListener('load', () => {
            setTimeout(() => {
                document.getElementById('loader').classList.add('hidden');
            }, 500);
        });

        // === МАТРИЦА ЭФФЕКТ ===
        const matrixCanvas = document.getElementById('matrixCanvas');
        const matrixCtx = matrixCanvas.getContext('2d');

        matrixCanvas.width = window.innerWidth;
        matrixCanvas.height = window.innerHeight;

        const matrixChars = '01アイウエオカキクケコサシスセソタチツテトナニヌネノハヒフヘホマミムメモヤユヨラリルレロワヲン';
        const matrixFontSize = 14;
        const matrixColumns = Math.floor(matrixCanvas.width / matrixFontSize);
        const matrixDrops = [];

        for (let i = 0; i < matrixColumns; i++) {
            matrixDrops[i] = Math.random() * -100;
        }

        function drawMatrix() {
            matrixCtx.fillStyle = 'rgba(0, 0, 0, 0.05)';
            matrixCtx.fillRect(0, 0, matrixCanvas.width, matrixCanvas.height);

            matrixCtx.fillStyle = '#0f0';
            matrixCtx.font = matrixFontSize + 'px monospace';

            for (let i = 0; i < matrixDrops.length; i++) {
                const char = matrixChars[Math.floor(Math.random() * matrixChars.length)];
                const x = i * matrixFontSize;
                const y = matrixDrops[i] * matrixFontSize;

                // Красный цвет для стиля Demon64k
                matrixCtx.fillStyle = `rgba(255, ${Math.floor(Math.random() * 100 + 50)}, ${Math.floor(Math.random() * 100 + 50)}, 0.8)`;
                matrixCtx.fillText(char, x, y);

                if (y > matrixCanvas.height && Math.random() > 0.975) {
                    matrixDrops[i] = 0;
                }

                matrixDrops[i]++;
            }
        }

        setInterval(drawMatrix, 50);

        // === ОГОНЬ ЭФФЕКТ ===
        const fireContainer = document.getElementById('fireContainer');

        // Создаём частицы огня
        for (let i = 0; i < 80; i++) {
            const fire = document.createElement('div');
            fire.className = 'fire-particle';
            fire.style.left = Math.random() * 100 + '%';
            fire.style.animationDelay = Math.random() * 4 + 's';
            fire.style.width = (Math.random() * 4 + 2) + 'px';
            fire.style.height = fire.style.width;
            fireContainer.appendChild(fire);
        }

        // Создаём искры
        for (let i = 0; i < 40; i++) {
            const ember = document.createElement('div');
            ember.className = 'ember';
            ember.style.left = Math.random() * 100 + '%';
            ember.style.animationDelay = Math.random() * 6 + 's';
            emberContainer = document.querySelector('.bg-effects');
            emberContainer.appendChild(ember);
        }

        // Адаптация матрицы под размер окна
        window.addEventListener('resize', () => {
            matrixCanvas.width = window.innerWidth;
            matrixCanvas.height = window.innerHeight;
        });

        // Анимация при скролле
        const observerOptions = { threshold: 0.1, rootMargin: '0px 0px -100px 0px' };
        const observer = new IntersectionObserver((entries) => {
            entries.forEach(entry => {
                if (entry.isIntersecting) {
                    entry.target.classList.add('active');
                }
            });
        }, observerOptions);

        document.querySelectorAll('.scroll-reveal').forEach(el => {
            observer.observe(el);
        });

        // Плавный скролл
        document.querySelectorAll('a[href^="#"]').forEach(anchor => {
            anchor.addEventListener('click', function (e) {
                e.preventDefault();
                const target = document.querySelector(this.getAttribute('href'));
                if (target) {
                    target.scrollIntoView({ behavior: 'smooth' });
                }
            });
        });

        // Parallax эффект
        document.addEventListener('mousemove', (e) => {
            const circles = document.querySelectorAll('.circle');
            const x = e.clientX / window.innerWidth;
            const y = e.clientY / window.innerHeight;

            circles.forEach((circle, index) => {
                const speed = (index + 1) * 20;
                circle.style.transform = `translate(${x * speed}px, ${y * speed}px)`;
            });
        });

        // Уведомление о копировании
        let copyTimeout = null;

        function showToast(message) {
            const toast = document.getElementById('copyToast');
            const messageEl = document.getElementById('copyMessage');
            messageEl.textContent = message;

            if (copyTimeout) {
                clearTimeout(copyTimeout);
                toast.classList.remove('show');
                toast.classList.add('hide');
            }

            setTimeout(() => {
                toast.classList.remove('hide');
                toast.classList.add('show');
            }, 50);

            copyTimeout = setTimeout(() => {
                toast.classList.remove('show');
                toast.classList.add('hide');
            }, 2500);
        }

        // Глобальное отслеживание копирования
        document.addEventListener('copy', (e) => {
            const selectedText = window.getSelection().toString().trim();
            if (selectedText.length > 0) {
                const displayText = selectedText.length > 30 
                    ? selectedText.substring(0, 30) + '...' 
                    : selectedText;
                showToast('📋 Скопировано: "' + displayText + '"');
            }
        });

        // Поддержка мобильных
        let touchStart = null;
        document.addEventListener('touchstart', (e) => {
            touchStart = Date.now();
        });

        document.addEventListener('touchend', (e) => {
            if (touchStart && Date.now() - touchStart > 500) {
                setTimeout(() => {
                    const selectedText = window.getSelection().toString().trim();
                    if (selectedText.length > 0) {
                        const displayText = selectedText.length > 30 
                            ? selectedText.substring(0, 30) + '...' 
                            : selectedText;
                        showToast('📋 Скопировано: "' + displayText + '"');
                    }
                }, 300);
            }
            touchStart = null;
        });
    </script>
</body>
</html>
"""


@app.get("/", response_class=HTMLResponse)
async def home():
    return HTML_CONTENT


if __name__ == "__main__":
    port = int(os.environ.get("PORT", 8000))
    print(f"🚀 Сервер запущен: http://127.0.0.1:{port}")
    print("🔥 Сайт с эффектами огня и матрицы готов!")
    uvicorn.run("main:app", host="0.0.0.0", port=port)