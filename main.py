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
    <link href="https://fonts.googleapis.com/css2?family=Inter:wght@300;400;600;700;900&display=swap" rel="stylesheet">
    <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.4.0/css/all.min.css">
    <style>
        * { margin: 0; padding: 0; box-sizing: border-box; user-select: text; }
        body {
            background: linear-gradient(135deg, #0a0a0a 0%, #1a1a2e 50%, #0f0f0f 100%);
            color: #e0e0e0;
            font-family: 'Inter', sans-serif;
            line-height: 1.6;
            overflow-x: hidden;
            min-height: 100vh;
            -webkit-user-select: text;
            -moz-user-select: text;
            -ms-user-select: text;
            user-select: text;
        }
        .bg-animation { position: fixed; top: 0; left: 0; width: 100%; height: 100%; z-index: -1; overflow: hidden; }
        .bg-animation .circle { position: absolute; border-radius: 50%; background: radial-gradient(circle, rgba(255,59,59,0.2) 0%, transparent 70%); animation: float 20s infinite ease-in-out; opacity: 0.4; }
        .bg-animation .circle:nth-child(1) { width: 400px; height: 400px; top: -200px; left: -200px; animation-delay: 0s; }
        .bg-animation .circle:nth-child(2) { width: 300px; height: 300px; top: 50%; right: -150px; animation-delay: 5s; }
        .bg-animation .circle:nth-child(3) { width: 250px; height: 250px; bottom: -125px; left: 30%; animation-delay: 10s; }
        @keyframes float { 0%, 100% { transform: translate(0, 0) scale(1); } 25% { transform: translate(30px, -30px) scale(1.1); } 50% { transform: translate(-20px, 20px) scale(0.9); } 75% { transform: translate(20px, 30px) scale(1.05); } }
        .particles { position: fixed; top: 0; left: 0; width: 100%; height: 100%; z-index: -1; pointer-events: none; }
        .particle { position: absolute; width: 2px; height: 2px; background: #ff6b8a; border-radius: 50%; opacity: 0.4; animation: particleFloat 15s infinite linear; }
        @keyframes particleFloat { 0% { transform: translateY(100vh) translateX(0); opacity: 0; } 10% { opacity: 0.4; } 90% { opacity: 0.4; } 100% { transform: translateY(-100vh) translateX(100px); opacity: 0; } }
        a { text-decoration: none; color: inherit; }
        .container { max-width: 1200px; margin: 0 auto; padding: 0 20px; }
        header { padding: 20px 0; position: fixed; top: 0; left: 0; right: 0; z-index: 1000; background: rgba(15, 15, 15, 0.85); backdrop-filter: blur(20px); border-bottom: 1px solid rgba(255, 107, 138, 0.15); animation: slideDown 0.8s ease-out; }
        @keyframes slideDown { from { transform: translateY(-100%); opacity: 0; } to { transform: translateY(0); opacity: 1; } }
        .nav-content { display: flex; justify-content: space-between; align-items: center; }
        .logo { font-size: 1.8rem; font-weight: 700; background: linear-gradient(135deg, #ff7b9a 0%, #ffb4c4 100%); -webkit-background-clip: text; -webkit-text-fill-color: transparent; background-clip: text; text-transform: uppercase; letter-spacing: 2px; display: flex; align-items: center; gap: 10px; }
        .logo i { font-size: 2rem; background: linear-gradient(135deg, #ff7b9a, #ffb4c4); -webkit-background-clip: text; -webkit-text-fill-color: transparent; filter: drop-shadow(0 0 8px rgba(255, 123, 154, 0.5)); }
        .nav-links { display: flex; gap: 15px; align-items: center; }
        
        /* ✨ УЛУЧШЕННЫЕ КНОПКИ ✨ */
        .btn {
            display: inline-flex;
            align-items: center;
            gap: 8px;
            padding: 10px 22px;
            border-radius: 14px;
            font-weight: 500;
            font-size: 0.95rem;
            transition: all 0.35s cubic-bezier(0.4, 0, 0.2, 1);
            position: relative;
            overflow: hidden;
            cursor: pointer;
            border: none;
            text-decoration: none;
        }
        
        .btn i {
            font-size: 1rem;
            transition: transform 0.3s ease;
        }
        
        .btn:hover i {
            transform: translateX(2px);
        }
        
        .btn::before {
            content: '';
            position: absolute;
            top: 0;
            left: -100%;
            width: 100%;
            height: 100%;
            background: linear-gradient(90deg, transparent, rgba(255,255,255,0.15), transparent);
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
        
        /* Telegram Button */
        .btn-telegram {
            background: linear-gradient(135deg, rgba(0, 136, 204, 0.2), rgba(0, 168, 232, 0.15));
            color: #7ec8ff;
            border: 1px solid rgba(126, 200, 255, 0.3);
        }
        
        .btn-telegram:hover {
            background: linear-gradient(135deg, rgba(0, 136, 204, 0.35), rgba(0, 168, 232, 0.25));
            color: #fff;
            border-color: rgba(126, 200, 255, 0.6);
            transform: translateY(-2px);
            box-shadow: 0 8px 25px rgba(0, 136, 204, 0.25);
        }
        
        /* Channel Button */
        .btn-channel-link {
            background: linear-gradient(135deg, rgba(255, 107, 138, 0.15), rgba(255, 140, 165, 0.1));
            color: #ffb4c4;
            border: 1px solid rgba(255, 140, 165, 0.25);
        }
        
        .btn-channel-link:hover {
            background: linear-gradient(135deg, rgba(255, 107, 138, 0.3), rgba(255, 140, 165, 0.2));
            color: #fff;
            border-color: rgba(255, 140, 165, 0.5);
            transform: translateY(-2px);
            box-shadow: 0 8px 25px rgba(255, 107, 138, 0.2);
        }
        
        /* Main CTA Button */
        .btn-main {
            display: inline-flex;
            align-items: center;
            gap: 12px;
            background: linear-gradient(135deg, #ff7b9a 0%, #ffb4c4 100%);
            color: #1a1a2e;
            padding: 16px 42px;
            font-size: 1.1rem;
            font-weight: 600;
            border-radius: 18px;
            border: none;
            cursor: pointer;
            box-shadow: 0 8px 30px rgba(255, 123, 154, 0.3);
            transition: all 0.4s cubic-bezier(0.4, 0, 0.2, 1);
            position: relative;
            overflow: hidden;
        }
        
        .btn-main i {
            font-size: 1.2rem;
            transition: transform 0.3s ease;
        }
        
        .btn-main:hover {
            transform: translateY(-4px);
            box-shadow: 0 15px 40px rgba(255, 123, 154, 0.45);
        }
        
        .btn-main:hover i {
            transform: translateX(3px);
        }
        
        .btn-main::after {
            content: '';
            position: absolute;
            top: 50%;
            left: 50%;
            width: 0;
            height: 0;
            border-radius: 50%;
            background: rgba(255, 255, 255, 0.4);
            transform: translate(-50%, -50%);
            transition: width 0.7s ease, height 0.7s ease;
            z-index: 0;
        }
        
        .btn-main:hover::after {
            width: 350px;
            height: 350px;
        }
        
        .btn-main > * {
            position: relative;
            z-index: 1;
        }
        
        /* Creator Section Buttons */
        .creator-links { display: flex; gap: 12px; justify-content: center; flex-wrap: wrap; margin-bottom: 20px; }
        
        .btn-creator {
            display: inline-flex;
            align-items: center;
            gap: 9px;
            padding: 12px 26px;
            border-radius: 16px;
            font-weight: 500;
            font-size: 0.95rem;
            transition: all 0.35s cubic-bezier(0.4, 0, 0.2, 1);
            position: relative;
            overflow: hidden;
            text-decoration: none;
            border: 1px solid transparent;
        }
        
        .btn-creator i {
            font-size: 1.1rem;
            transition: transform 0.3s ease;
        }
        
        .btn-creator:hover i {
            transform: translateX(2px) scale(1.1);
        }
        
        .btn-creator::before {
            content: '';
            position: absolute;
            top: 0;
            left: -100%;
            width: 100%;
            height: 100%;
            background: linear-gradient(90deg, transparent, rgba(255,255,255,0.2), transparent);
            transition: left 0.6s ease;
            z-index: 0;
        }
        
        .btn-creator:hover::before {
            left: 100%;
        }
        
        .btn-creator > * {
            position: relative;
            z-index: 1;
        }
        
        /* Telegram Creator Button */
        .btn-creator-telegram {
            background: linear-gradient(135deg, rgba(0, 136, 204, 0.25), rgba(0, 168, 232, 0.2));
            color: #8ad4ff;
            border-color: rgba(138, 212, 255, 0.35);
        }
        
        .btn-creator-telegram:hover {
            background: linear-gradient(135deg, rgba(0, 136, 204, 0.4), rgba(0, 168, 232, 0.3));
            color: #fff;
            border-color: rgba(138, 212, 255, 0.6);
            transform: translateY(-3px);
            box-shadow: 0 10px 30px rgba(0, 136, 204, 0.3);
        }
        
        /* Channel Creator Button */
        .btn-creator-channel {
            background: linear-gradient(135deg, rgba(255, 107, 138, 0.2), rgba(255, 140, 165, 0.15));
            color: #ffc4d4;
            border-color: rgba(255, 164, 184, 0.3);
        }
        
        .btn-creator-channel:hover {
            background: linear-gradient(135deg, rgba(255, 107, 138, 0.35), rgba(255, 140, 165, 0.25));
            color: #fff;
            border-color: rgba(255, 164, 184, 0.55);
            transform: translateY(-3px);
            box-shadow: 0 10px 30px rgba(255, 107, 138, 0.25);
        }
        
        /* Social Icons */
        .creator-social { display: flex; gap: 14px; justify-content: center; margin-top: 18px; }
        
        .creator-social a {
            width: 48px;
            height: 48px;
            border-radius: 14px;
            display: flex;
            align-items: center;
            justify-content: center;
            font-size: 1.3rem;
            transition: all 0.35s cubic-bezier(0.4, 0, 0.2, 1);
            position: relative;
            overflow: hidden;
            border: 1px solid transparent;
        }
        
        .creator-social a i {
            position: relative;
            z-index: 1;
            transition: transform 0.3s ease;
        }
        
        .creator-social a:hover i {
            transform: scale(1.15);
        }
        
        .creator-social a::before {
            content: '';
            position: absolute;
            top: 0;
            left: -100%;
            width: 100%;
            height: 100%;
            background: linear-gradient(90deg, transparent, rgba(255,255,255,0.25), transparent);
            transition: left 0.5s ease;
            z-index: 0;
        }
        
        .creator-social a:hover::before {
            left: 100%;
        }
        
        .creator-social a > * {
            position: relative;
            z-index: 1;
        }
        
        /* GitHub */
        .creator-social .github {
            background: linear-gradient(135deg, rgba(45, 50, 58, 0.4), rgba(65, 75, 88, 0.3));
            color: #c9d1d9;
            border-color: rgba(201, 209, 217, 0.25);
        }
        
        .creator-social .github:hover {
            background: linear-gradient(135deg, rgba(45, 50, 58, 0.6), rgba(65, 75, 88, 0.45));
            color: #fff;
            border-color: rgba(201, 209, 217, 0.5);
            transform: translateY(-4px);
            box-shadow: 0 10px 28px rgba(36, 41, 46, 0.4);
        }
        
        /* Pinterest */
        .creator-social .pinterest {
            background: linear-gradient(135deg, rgba(230, 0, 35, 0.25), rgba(255, 40, 75, 0.2));
            color: #ffc4d4;
            border-color: rgba(255, 164, 184, 0.3);
        }
        
        .creator-social .pinterest:hover {
            background: linear-gradient(135deg, rgba(230, 0, 35, 0.4), rgba(255, 40, 75, 0.3));
            color: #fff;
            border-color: rgba(255, 164, 184, 0.55);
            transform: translateY(-4px);
            box-shadow: 0 10px 28px rgba(230, 0, 35, 0.35);
        }
        
        /* Channel Section Button */
        .btn-channel {
            display: inline-flex;
            align-items: center;
            gap: 11px;
            background: linear-gradient(135deg, rgba(0, 136, 204, 0.25), rgba(0, 168, 232, 0.2));
            color: #8ad4ff;
            padding: 15px 38px;
            border-radius: 17px;
            font-size: 1.05rem;
            font-weight: 500;
            border: 1px solid rgba(138, 212, 255, 0.3);
            transition: all 0.4s cubic-bezier(0.4, 0, 0.2, 1);
            position: relative;
            overflow: hidden;
        }
        
        .btn-channel i {
            font-size: 1.3rem;
            transition: transform 0.3s ease;
        }
        
        .btn-channel:hover {
            background: linear-gradient(135deg, rgba(0, 136, 204, 0.4), rgba(0, 168, 232, 0.3));
            color: #fff;
            border-color: rgba(138, 212, 255, 0.6);
            transform: translateY(-4px);
            box-shadow: 0 12px 35px rgba(0, 136, 204, 0.3);
        }
        
        .btn-channel:hover i {
            transform: translateX(3px);
        }
        
        .btn-channel::after {
            content: '';
            position: absolute;
            top: 50%;
            left: 50%;
            width: 0;
            height: 0;
            border-radius: 50%;
            background: rgba(255, 255, 255, 0.25);
            transform: translate(-50%, -50%);
            transition: width 0.6s ease, height 0.6s ease;
            z-index: 0;
        }
        
        .btn-channel:hover::after {
            width: 320px;
            height: 320px;
        }
        
        .btn-channel > * {
            position: relative;
            z-index: 1;
        }
        
        /* Footer Social Links */
        .social-links { margin-bottom: 30px; display: flex; justify-content: center; gap: 18px; }
        
        .social-links a {
            width: 54px;
            height: 54px;
            background: rgba(255, 123, 154, 0.12);
            border: 1px solid rgba(255, 140, 165, 0.25);
            border-radius: 16px;
            display: flex;
            align-items: center;
            justify-content: center;
            font-size: 1.4rem;
            color: #ffb4c4;
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
            top: 0;
            left: -100%;
            width: 100%;
            height: 100%;
            background: linear-gradient(90deg, transparent, rgba(255,255,255,0.2), transparent);
            transition: left 0.5s ease;
            z-index: 0;
        }
        
        .social-links a:hover::before {
            left: 100%;
        }
        
        .social-links a:hover {
            background: linear-gradient(135deg, rgba(255, 107, 138, 0.3), rgba(255, 140, 165, 0.2));
            color: #fff;
            border-color: rgba(255, 164, 184, 0.5);
            transform: translateY(-5px) scale(1.08);
            box-shadow: 0 12px 30px rgba(255, 107, 138, 0.3);
        }
        
        .social-links a:hover i {
            transform: scale(1.1);
        }
        
        .social-links a > * {
            position: relative;
            z-index: 1;
        }
        
        /* Hero Section */
        .hero { padding: 180px 0 120px; text-align: center; position: relative; }
        .hero-badge { display: inline-flex; align-items: center; gap: 9px; background: rgba(255, 123, 154, 0.15); border: 1px solid rgba(255, 140, 165, 0.25); padding: 9px 19px; border-radius: 16px; color: #ffc4d4; font-size: 0.9rem; margin-bottom: 25px; animation: fadeInUp 0.8s ease-out; }
        .hero-badge i { animation: badgeSpin 4s linear infinite; }
        @keyframes badgeSpin { 0% { transform: rotate(0deg); } 100% { transform: rotate(360deg); } }
        .hero h1 { font-size: 4rem; font-weight: 800; margin-bottom: 25px; background: linear-gradient(135deg, #fff 0%, #ff7b9a 50%, #ffb4c4 100%); -webkit-background-clip: text; -webkit-text-fill-color: transparent; background-clip: text; animation: titlePulse 4s ease-in-out infinite; line-height: 1.2; }
        @keyframes titlePulse { 0%, 100% { transform: scale(1); } 50% { transform: scale(1.015); } }
        .hero p { font-size: 1.25rem; color: #b8b8d0; max-width: 700px; margin: 0 auto 50px; animation: fadeInUp 1s ease-out 0.3s both; }
        
        @keyframes fadeInUp { from { opacity: 0; transform: translateY(25px); } to { opacity: 1; transform: translateY(0); } }
        
        /* What is ID Section */
        .what-is-id { padding: 100px 0; background: rgba(20, 20, 20, 0.5); position: relative; }
        .id-card { max-width: 900px; margin: 0 auto; background: linear-gradient(135deg, rgba(255, 107, 138, 0.08), rgba(26, 26, 26, 0.7)); border: 1px solid rgba(255, 140, 165, 0.2); border-radius: 28px; padding: 55px 38px; backdrop-filter: blur(15px); animation: fadeInUp 1s ease-out; box-shadow: 0 15px 50px rgba(255, 107, 138, 0.12); }
        .id-card h2 { font-size: 2.3rem; margin-bottom: 28px; background: linear-gradient(135deg, #fff, #ff7b9a); -webkit-background-clip: text; -webkit-text-fill-color: transparent; background-clip: text; text-align: center; display: flex; align-items: center; justify-content: center; gap: 14px; }
        .id-card h2 i { font-size: 2.5rem; animation: questionBounce 2.5s ease-in-out infinite; background: linear-gradient(135deg, #ff7b9a, #ffb4c4); -webkit-background-clip: text; -webkit-text-fill-color: transparent; }
        @keyframes questionBounce { 0%, 100% { transform: translateY(0); } 50% { transform: translateY(-8px); } }
        .id-card > p { color: #b8b8d0; font-size: 1.05rem; line-height: 1.75; margin-bottom: 38px; text-align: center; }
        .id-uses { display: grid; grid-template-columns: repeat(auto-fit, minmax(240px, 1fr)); gap: 22px; margin-top: 35px; }
        .use-item { background: rgba(26, 26, 26, 0.6); padding: 28px 22px; border-radius: 18px; border: 1px solid rgba(255, 140, 165, 0.15); transition: all 0.35s ease; animation: fadeInUp 1s ease-out both; text-align: center; }
        .use-item:nth-child(1) { animation-delay: 0.1s; } .use-item:nth-child(2) { animation-delay: 0.2s; } .use-item:nth-child(3) { animation-delay: 0.3s; } .use-item:nth-child(4) { animation-delay: 0.4s; }
        .use-item:hover { border-color: rgba(255, 140, 165, 0.4); transform: translateY(-8px); box-shadow: 0 12px 32px rgba(255, 107, 138, 0.2); }
        .use-icon { width: 72px; height: 72px; margin: 0 auto 18px; background: linear-gradient(135deg, rgba(255, 107, 138, 0.15), rgba(255, 140, 165, 0.1)); border-radius: 18px; display: flex; align-items: center; justify-content: center; font-size: 2.2rem; position: relative; transition: all 0.35s ease; }
        .use-icon::before { content: ''; position: absolute; width: 100%; height: 100%; border-radius: 18px; background: linear-gradient(135deg, rgba(255, 107, 138, 0.2), rgba(255, 140, 165, 0.15)); opacity: 0; transition: opacity 0.3s ease; z-index: -1; }
        .use-item:hover .use-icon { transform: scale(1.08) rotate(3deg); }
        .use-item:hover .use-icon::before { opacity: 1; }
        .use-icon i { background: linear-gradient(135deg, #ff7b9a, #ffb4c4); -webkit-background-clip: text; -webkit-text-fill-color: transparent; }
        .use-item h3 { color: #ffb4c4; font-size: 1.2rem; margin-bottom: 11px; font-weight: 600; }
        .use-item p { color: #9a9ab5; font-size: 0.93rem; line-height: 1.55; }
        
        /* Creator Section */
        .creator-section { padding: 100px 0; background: rgba(15, 15, 15, 0.75); position: relative; }
        .creator-card { max-width: 780px; margin: 0 auto; background: linear-gradient(135deg, rgba(255, 107, 138, 0.1), rgba(26, 26, 26, 0.75)); border: 1px solid rgba(255, 140, 165, 0.22); border-radius: 28px; padding: 55px 36px; text-align: center; backdrop-filter: blur(15px); animation: fadeInUp 1s ease-out; box-shadow: 0 18px 55px rgba(255, 107, 138, 0.15); }
        .creator-avatar-frame { position: relative; width: 145px; height: 145px; margin: 0 auto 28px; border-radius: 50%; padding: 4px; background: linear-gradient(135deg, #ff7b9a, #ffb4c4); box-shadow: 0 8px 40px rgba(255, 123, 154, 0.4); animation: avatarPulse 3.5s ease-in-out infinite; }
        .creator-avatar-window { width: 100%; height: 100%; border-radius: 50%; background: linear-gradient(135deg, #1a1a2e, #0f0f0f); display: flex; align-items: center; justify-content: center; overflow: hidden; position: relative; border: 2px solid rgba(255, 255, 255, 0.12); }
        .creator-avatar-window img { width: 100%; height: 100%; object-fit: cover; border-radius: 50%; transition: transform 0.4s ease; }
        .creator-avatar-window:hover img { transform: scale(1.08); }
        @keyframes avatarPulse { 0%, 100% { transform: scale(1); box-shadow: 0 8px 40px rgba(255, 123, 154, 0.4); } 50% { transform: scale(1.03); box-shadow: 0 12px 50px rgba(255, 123, 154, 0.55); } }
        .creator-card h2 { font-size: 2.3rem; margin-bottom: 14px; background: linear-gradient(135deg, #fff, #ff7b9a); -webkit-background-clip: text; -webkit-text-fill-color: transparent; background-clip: text; }
        .creator-card .username { color: #ffc4d4; font-size: 1.25rem; margin-bottom: 24px; font-weight: 600; }
        .creator-card p { color: #b8b8d0; font-size: 1.05rem; line-height: 1.7; margin-bottom: 28px; }
        
        /* Bot Info Section */
        .bot-info { padding: 75px 0; background: rgba(20, 20, 20, 0.45); position: relative; }
        .info-grid { display: grid; grid-template-columns: repeat(auto-fit, minmax(270px, 1fr)); gap: 26px; margin-top: 45px; }
        .info-card { background: rgba(26, 26, 26, 0.65); padding: 32px; border-radius: 19px; border: 1px solid rgba(255, 140, 165, 0.16); transition: all 0.4s ease; backdrop-filter: blur(10px); animation: fadeInUp 1s ease-out both; display: flex; align-items: center; gap: 22px; }
        .info-card:nth-child(1) { animation-delay: 0.1s; } .info-card:nth-child(2) { animation-delay: 0.2s; } .info-card:nth-child(3) { animation-delay: 0.3s; } .info-card:nth-child(4) { animation-delay: 0.4s; }
        .info-card:hover { border-color: rgba(255, 140, 165, 0.4); transform: translateY(-9px); box-shadow: 0 18px 38px rgba(255, 107, 138, 0.22); }
        .info-icon { width: 66px; height: 66px; background: linear-gradient(135deg, rgba(255, 107, 138, 0.18), rgba(255, 140, 165, 0.12)); border-radius: 17px; display: flex; align-items: center; justify-content: center; font-size: 2rem; flex-shrink: 0; transition: all 0.35s ease; position: relative; overflow: hidden; }
        .info-icon::after { content: ''; position: absolute; width: 100%; height: 100%; background: radial-gradient(circle, rgba(255,255,255,0.25) 0%, transparent 70%); opacity: 0; transition: opacity 0.3s ease; }
        .info-card:hover .info-icon { transform: scale(1.08) rotate(-4deg); }
        .info-card:hover .info-icon::after { opacity: 1; }
        .info-icon i { background: linear-gradient(135deg, #ff7b9a, #ffb4c4); -webkit-background-clip: text; -webkit-text-fill-color: transparent; }
        .info-content h3 { color: #8a8aa5; font-size: 0.88rem; margin-bottom: 7px; text-transform: uppercase; letter-spacing: 0.8px; font-weight: 600; }
        .info-content p { color: #fff; font-size: 1.15rem; font-weight: 500; }
        
        /* Features Section */
        .features { padding: 95px 0; background: rgba(15, 15, 15, 0.75); position: relative; }
        .section-title { text-align: center; font-size: 2.8rem; font-weight: 750; margin-bottom: 18px; background: linear-gradient(135deg, #fff 0%, #ff7b9a 100%); -webkit-background-clip: text; -webkit-text-fill-color: transparent; background-clip: text; animation: fadeInUp 1s ease-out; }
        .section-subtitle { text-align: center; color: #9a9ab5; font-size: 1.05rem; margin-bottom: 55px; animation: fadeInUp 1s ease-out 0.2s both; }
        .grid { display: grid; grid-template-columns: repeat(auto-fit, minmax(300px, 1fr)); gap: 35px; }
        .card { background: rgba(26, 26, 26, 0.55); padding: 42px 32px; border-radius: 24px; border: 1px solid rgba(255, 140, 165, 0.12); transition: all 0.4s cubic-bezier(0.4, 0, 0.2, 1); position: relative; overflow: hidden; backdrop-filter: blur(10px); animation: fadeInUp 1s ease-out both; text-align: center; }
        .card:nth-child(1) { animation-delay: 0.1s; } .card:nth-child(2) { animation-delay: 0.2s; } .card:nth-child(3) { animation-delay: 0.3s; } .card:nth-child(4) { animation-delay: 0.4s; }
        .card::before { content: ''; position: absolute; top: 0; left: -100%; width: 100%; height: 100%; background: linear-gradient(90deg, transparent, rgba(255, 140, 165, 0.08), transparent); transition: left 0.7s ease; }
        .card:hover::before { left: 100%; }
        .card:hover { border-color: rgba(255, 140, 165, 0.35); transform: translateY(-13px); box-shadow: 0 22px 45px rgba(255, 107, 138, 0.22); }
        .card-icon { font-size: 3.6rem; margin-bottom: 22px; display: inline-block; animation: iconBounce 2.5s ease-in-out infinite; background: linear-gradient(135deg, #ff7b9a, #ffb4c4); -webkit-background-clip: text; -webkit-text-fill-color: transparent; }
        @keyframes iconBounce { 0%, 100% { transform: translateY(0) rotate(0deg); } 25% { transform: translateY(-8px) rotate(-3deg); } 75% { transform: translateY(-4px) rotate(3deg); } }
        .card h3 { color: #ffb4c4; margin-bottom: 14px; font-size: 1.55rem; font-weight: 650; }
        .card p { color: #a0a0b8; font-size: 0.98rem; line-height: 1.7; }
        
        /* Channel Section */
        .channel-section { padding: 95px 0; background: linear-gradient(135deg, rgba(255, 107, 138, 0.08), rgba(26, 26, 46, 0.75)); text-align: center; position: relative; overflow: hidden; }
        .channel-section::before { content: ''; position: absolute; top: -50%; left: -50%; width: 200%; height: 200%; background: radial-gradient(circle, rgba(255, 107, 138, 0.08) 0%, transparent 70%); animation: rotate 35s linear infinite; }
        @keyframes rotate { 0% { transform: rotate(0deg); } 100% { transform: rotate(360deg); } }
        .channel-content { position: relative; z-index: 1; }
        .channel-section h2 { font-size: 2.3rem; margin-bottom: 18px; color: #fff; animation: fadeInUp 1s ease-out; display: flex; align-items: center; justify-content: center; gap: 14px; }
        .channel-section h2 i { font-size: 2.5rem; animation: megaphoneWave 2.5s ease-in-out infinite; background: linear-gradient(135deg, #7ec8ff, #a8e6ff); -webkit-background-clip: text; -webkit-text-fill-color: transparent; }
        @keyframes megaphoneWave { 0%, 100% { transform: rotate(-8deg) scale(1); } 50% { transform: rotate(8deg) scale(1.08); } }
        .channel-section p { color: #b8b8d0; font-size: 1.15rem; margin-bottom: 38px; max-width: 580px; margin-left: auto; margin-right: auto; animation: fadeInUp 1s ease-out 0.2s both; }
        
        /* Footer */
        footer { padding: 55px 0 28px; text-align: center; border-top: 1px solid rgba(255, 140, 165, 0.12); background: rgba(10, 10, 10, 0.92); position: relative; }
        .footer-content { position: relative; z-index: 1; }
        footer p { color: #7a7a95; margin-bottom: 9px; font-size: 0.93rem; }
        .creator-info { color: #8a8aa5; font-size: 0.92rem; margin-top: 18px; }
        .creator-info a { color: #ffb4c4; font-weight: 500; transition: all 0.3s ease; }
        .creator-info a:hover { color: #ffc4d4; text-decoration: none; }
        
        /* Scroll Animation */
        .scroll-reveal { opacity: 0; transform: translateY(45px); transition: all 0.75s ease-out; }
        .scroll-reveal.active { opacity: 1; transform: translateY(0); }
        
        /* Responsive */
        @media (max-width: 768px) {
            .hero h1 { font-size: 2.4rem; }
            .section-title { font-size: 1.9rem; }
            .nav-content { flex-direction: column; gap: 14px; }
            .hero { padding: 135px 0 75px; }
            .creator-card, .id-card { padding: 38px 24px; }
            .creator-card h2, .id-card h2 { font-size: 1.85rem; }
            .info-grid { grid-template-columns: 1fr; }
            .id-uses { grid-template-columns: 1fr; }
            .use-icon { width: 64px; height: 64px; font-size: 1.9rem; }
            .card-icon { font-size: 3rem; }
            .creator-avatar-frame { width: 125px; height: 125px; }
            .creator-links { flex-direction: column; align-items: center; }
            .btn-creator { width: 100%; max-width: 280px; justify-content: center; }
            .btn-main { padding: 14px 36px; font-size: 1rem; }
        }
        
        /* Loading Animation */
        .loader { position: fixed; top: 0; left: 0; width: 100%; height: 100%; background: #0a0a0a; display: flex; justify-content: center; align-items: center; z-index: 9999; transition: opacity 0.5s ease; }
        .loader.hidden { opacity: 0; pointer-events: none; }
        .loader-circle { width: 56px; height: 56px; border: 3px solid rgba(255, 123, 154, 0.15); border-top-color: #ff7b9a; border-radius: 50%; animation: spin 1s linear infinite; box-shadow: 0 0 18px rgba(255, 123, 154, 0.25); }
        @keyframes spin { to { transform: rotate(360deg); } }
        
        /* ✨ COPY TOAST NOTIFICATION ✨ */
        .copy-toast {
            position: fixed;
            bottom: 28px;
            left: 50%;
            transform: translateX(-50%) translateY(100px);
            background: linear-gradient(135deg, #ff7b9a, #ffb4c4);
            color: #1a1a2e;
            padding: 14px 28px;
            border-radius: 16px;
            font-weight: 500;
            font-size: 0.95rem;
            box-shadow: 0 10px 35px rgba(255, 123, 154, 0.4);
            display: flex;
            align-items: center;
            gap: 11px;
            z-index: 10000;
            opacity: 0;
            transition: all 0.4s cubic-bezier(0.4, 0, 0.2, 1);
            backdrop-filter: blur(12px);
            border: 1px solid rgba(255, 255, 255, 0.25);
            pointer-events: none;
        }
        
        .copy-toast.show { transform: translateX(-50%) translateY(0); opacity: 1; }
        .copy-toast i { font-size: 1.2rem; animation: toastIconBounce 0.6s ease-in-out; }
        @keyframes toastIconBounce { 0% { transform: scale(0) rotate(-180deg); } 50% { transform: scale(1.25) rotate(8deg); } 100% { transform: scale(1) rotate(0deg); } }
        .copy-toast::before { content: ''; position: absolute; top: 50%; left: 50%; width: 0; height: 0; border-radius: 50%; background: rgba(255, 255, 255, 0.35); transform: translate(-50%, -50%); transition: width 0.6s ease, height 0.6s ease; z-index: -1; }
        .copy-toast.show::before { width: 380px; height: 380px; }
        .copy-toast.hide { transform: translateX(-50%) translateY(-18px); opacity: 0; }
        
        /* Подсветка при выделении */
        ::selection { background: rgba(255, 123, 154, 0.35); color: white; }
        ::-moz-selection { background: rgba(255, 123, 154, 0.35); color: white; }
    </style>
</head>
<body>
    <!-- Copy Toast Notification -->
    <div class="copy-toast" id="copyToast">
        <i class="fas fa-check-circle"></i>
        <span id="copyMessage">Скопировано!</span>
    </div>

    <div class="loader" id="loader"><div class="loader-circle"></div></div>
    <div class="bg-animation"><div class="circle"></div><div class="circle"></div><div class="circle"></div></div>
    <div class="particles" id="particles"></div>
    
    <header>
        <div class="container nav-content">
            <div class="logo"><i class="fas fa-robot"></i> Demon64k Bot</div>
            <div class="nav-links">
                <a href="#features" class="btn btn-channel-link"><i class="fas fa-star"></i> Возможности</a>
                <a href="https://t.me/Demon64k_information_bot" class="btn btn-telegram"><i class="fab fa-telegram-plane"></i> Запустить</a>
            </div>
        </div>
    </header>
    
    <section class="hero">
        <div class="container">
            <div class="hero-badge"><i class="fas fa-search"></i> Поиск информации</div>
            <h1>Demon64k ID Bot</h1>
            <p>Бот для поиска базовой информации о пользователях в Telegram: ID, никнейм, язык, юзернейм. Быстро, удобно и бесплатно!</p>
            <a href="https://t.me/Demon64k_information_bot" class="btn-main"><i class="fab fa-telegram-plane"></i> Запустить бота</a>
        </div>
    </section>
    
    <section class="what-is-id">
        <div class="container">
            <div class="id-card scroll-reveal">
                <h2><i class="fas fa-question-circle"></i> Зачем нужен ID?</h2>
                <p>Для обычных пользователей он навряд ли понадобится, но вот для разработчиков телеграм-ботов он во многом может пригодиться:</p>
                <div class="id-uses">
                    <div class="use-item"><div class="use-icon"><i class="fas fa-code"></i></div><h3>Создание ботов</h3><p>Сделать похожий бот для своих проектов и задач</p></div>
                    <div class="use-item"><div class="use-icon"><i class="fas fa-bell"></i></div><h3>Уведомления</h3><p>Отправка уведомлений о новых пользователях</p></div>
                    <div class="use-item"><div class="use-icon"><i class="fas fa-users"></i></div><h3>Идентификация</h3><p>Не путать пользователей с одинаковыми именами</p></div>
                    <div class="use-item"><div class="use-icon"><i class="fas fa-cogs"></i></div><h3>И другое</h3><p>Множество применений для разработки</p></div>
                </div>
            </div>
        </div>
    </section>
    
    <section class="bot-info">
        <div class="container">
            <h2 class="section-title scroll-reveal">Что показывает бот</h2>
            <div class="info-grid">
                <div class="info-card scroll-reveal"><div class="info-icon"><i class="fas fa-fingerprint"></i></div><div class="info-content"><h3>ID пользователя</h3><p>Уникальный идентификатор</p></div></div>
                <div class="info-card scroll-reveal"><div class="info-icon"><i class="fas fa-at"></i></div><div class="info-content"><h3>Юзернейм</h3><p>Имя пользователя @username</p></div></div>
                <div class="info-card scroll-reveal"><div class="info-icon"><i class="fas fa-user-tag"></i></div><div class="info-content"><h3>Никнейм</h3><p>Отображаемое имя</p></div></div>
                <div class="info-card scroll-reveal"><div class="info-icon"><i class="fas fa-language"></i></div><div class="info-content"><h3>Язык</h3><p>Язык интерфейса Telegram</p></div></div>
            </div>
        </div>
    </section>
    
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
                <p>Разработчик и основатель Demon64k Information Bot. Создаю удобные решения для Telegram. Всегда открыт к сотрудничеству!</p>
                
                <div class="creator-links">
                    <a href="https://t.me/Trump1238" target="_blank" class="btn-creator btn-creator-telegram">
                        <i class="fab fa-telegram-plane"></i> Telegram
                    </a>
                    <a href="https://t.me/Demon64k_poisk" target="_blank" class="btn-creator btn-creator-channel">
                        <i class="fas fa-broadcast-tower"></i> Канал
                    </a>
                </div>
                
                <div class="creator-social">
                    <a href="https://github.com/demon64k" target="_blank" class="github" title="GitHub">
                        <i class="fab fa-github"></i>
                    </a>
                    <a href="https://pin.it/6JRrwXT1O" target="_blank" class="pinterest" title="Pinterest">
                        <i class="fab fa-pinterest"></i>
                    </a>
                </div>
            </div>
        </div>
    </section>
    
    <section class="features" id="features">
        <div class="container">
            <h2 class="section-title scroll-reveal">Преимущества</h2>
            <p class="section-subtitle scroll-reveal">Почему стоит использовать наш бот</p>
            <div class="grid">
                <div class="card scroll-reveal"><span class="card-icon"><i class="fas fa-bolt"></i></span><h3>Быстрый ответ</h3><p>Мгновенное получение информации без задержек</p></div>
                <div class="card scroll-reveal"><span class="card-icon"><i class="fas fa-shield-alt"></i></span><h3>Безопасность</h3><p>Бот не хранит личные данные</p></div>
                <div class="card scroll-reveal"><span class="card-icon"><i class="fas fa-mobile-alt"></i></span><h3>Удобство</h3><p>Управление прямо в Telegram</p></div>
                <div class="card scroll-reveal"><span class="card-icon"><i class="fas fa-gift"></i></span><h3>Бесплатно</h3><p>Полный доступ без ограничений</p></div>
            </div>
        </div>
    </section>
    
    <section class="channel-section">
        <div class="container channel-content">
            <h2 class="scroll-reveal"><i class="fas fa-bullhorn"></i> Наш канал</h2>
            <p class="scroll-reveal">Подпишитесь на @Demon64k_poisk, чтобы быть в курсе обновлений</p>
            <a href="https://t.me/Demon64k_poisk" target="_blank" class="btn-channel scroll-reveal">
                <i class="fab fa-telegram-plane"></i> Подписаться
            </a>
        </div>
    </section>
    
    <footer>
        <div class="container footer-content">
            <div class="social-links">
                <a href="https://t.me/Demon64k_information_bot" title="Запустить бота"><i class="fab fa-telegram-plane"></i></a>
                <a href="https://t.me/Demon64k_poisk" title="Наш канал"><i class="fas fa-broadcast-tower"></i></a>
                <a href="https://t.me/Trump1238" title="Создатель"><i class="fas fa-user-shield"></i></a>
                <a href="https://github.com/demon64k" target="_blank" title="GitHub"><i class="fab fa-github"></i></a>
                <a href="https://pin.it/6JRrwXT1O" target="_blank" title="Pinterest"><i class="fab fa-pinterest"></i></a>
            </div>
            <p>&copy; 2026 Demon64k Information Bot. Все права защищены.</p>
            <div class="creator-info">Создатель: <a href="https://t.me/Trump1238" target="_blank">@Trump1238</a></div>
        </div>
    </footer>
    
    <script>
        window.addEventListener('load', () => { setTimeout(() => { document.getElementById('loader').classList.add('hidden'); }, 500); });
        const particlesContainer = document.getElementById('particles');
        for (let i = 0; i < 45; i++) { const particle = document.createElement('div'); particle.className = 'particle'; particle.style.left = Math.random() * 100 + '%'; particle.style.animationDelay = Math.random() * 15 + 's'; particle.style.animationDuration = (Math.random() * 10 + 10) + 's'; particlesContainer.appendChild(particle); }
        const observerOptions = { threshold: 0.1, rootMargin: '0px 0px -100px 0px' };
        const observer = new IntersectionObserver((entries) => { entries.forEach(entry => { if (entry.isIntersecting) { entry.target.classList.add('active'); } }); }, observerOptions);
        document.querySelectorAll('.scroll-reveal').forEach(el => { observer.observe(el); });
        document.querySelectorAll('a[href^="#"]').forEach(anchor => { anchor.addEventListener('click', function (e) { e.preventDefault(); const target = document.querySelector(this.getAttribute('href')); if (target) { target.scrollIntoView({ behavior: 'smooth' }); } }); });
        document.addEventListener('mousemove', (e) => { const circles = document.querySelectorAll('.circle'); const x = e.clientX / window.innerWidth; const y = e.clientY / window.innerHeight; circles.forEach((circle, index) => { const speed = (index + 1) * 18; circle.style.transform = `translate(${x * speed}px, ${y * speed}px)`; }); });
        
        let copyTimeout = null;
        function showToast(message) {
            const toast = document.getElementById('copyToast');
            const messageEl = document.getElementById('copyMessage');
            messageEl.textContent = message;
            if (copyTimeout) { clearTimeout(copyTimeout); toast.classList.remove('show'); toast.classList.add('hide'); }
            setTimeout(() => { toast.classList.remove('hide'); toast.classList.add('show'); }, 50);
            copyTimeout = setTimeout(() => { toast.classList.remove('show'); toast.classList.add('hide'); }, 2300);
        }
        
        document.addEventListener('copy', (e) => {
            const selectedText = window.getSelection().toString().trim();
            if (selectedText.length > 0) {
                const displayText = selectedText.length > 28 ? selectedText.substring(0, 28) + '...' : selectedText;
                showToast('📋 Скопировано: "' + displayText + '"');
            }
        });
        
        let touchStart = null;
        document.addEventListener('touchstart', (e) => { touchStart = Date.now(); });
        document.addEventListener('touchend', (e) => {
            if (touchStart && Date.now() - touchStart > 500) {
                setTimeout(() => {
                    const selectedText = window.getSelection().toString().trim();
                    if (selectedText.length > 0) {
                        const displayText = selectedText.length > 28 ? selectedText.substring(0, 28) + '...' : selectedText;
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
    print("✨ Сайт с элегантными кнопками готов!")
    uvicorn.run("main:app", host="0.0.0.0", port=port)