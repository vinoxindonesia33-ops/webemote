from flask import Flask, render_template, request, jsonify
import requests
import json
import os

app = Flask(__name__)

# استخدام متغير البيئة للجلسة أو القيمة الافتراضية
SESSION_COOKIE = os.environ.get('FF_SESSION_COOKIE', 'eyJsb2dnZWQiOnRydWUsInVzZXJfaWQiOiIzMzIwNDQ2Mjk5IiwidXNlcl9uYW1lIjoiVklOT1gifQ.aVUdUw.NfvNNP5DvpnWw2ydhcVvAv0ygk0')

cookies = {
    "session": SESSION_COOKIE,
}

headers = {
    "Host": "m2.0xarm.com",
    "Connection": "keep-alive",
    "sec-ch-ua-platform": "\"Android\"",
    "User-Agent": "Mozilla/5.0 (Linux; Android 14; Infinix X6882 Build/UP1A.231005.007) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/143.0.7499.146 Mobile Safari/537.36",
    "sec-ch-ua": "\"Android WebView\";v=\"143\", \"Chromium\";v=\"143\", \"Not A(Brand\";v=\"24\"",
    "Content-Type": "application/json",
    "sec-ch-ua-mobile": "?1",
    "Accept": "*/*",
    "Origin": "https://m2.0xarm.com",
    "X-Requested-With": "mark.via.gp",
    "Sec-Fetch-Site": "same-origin",
    "Sec-Fetch-Mode": "cors",
    "Sec-Fetch-Dest": "empty",
    "Referer": "https://m2.0xarm.com/dashboard",
    "Accept-Encoding": "gzip, deflate, br, zstd",
    "Accept-Language": "en-US,en;q=0.9,ar-TN;q=0.8,ar;q=0.7"
}

# قائمة الرقصات مع صور أكبر وأسماء مناسبة
emotes = [
    {"id": "909000001", "name": "رقصة التحية", "img": "https://cdn.jsdelivr.net/gh/ShahGCreator/icon@main/PNG/909000001.png"},
    {"id": "909000002", "name": "رقصة الضحك", "img": "https://cdn.jsdelivr.net/gh/ShahGCreator/icon@main/PNG/909000002.png"},
    {"id": "909000003", "name": "رقصة الاستفزاز", "img": "https://cdn.jsdelivr.net/gh/ShahGCreator/icon@main/PNG/909000003.png"},
    {"id": "909042007", "name": "رقصة النحت", "img": "https://cdn.jsdelivr.net/gh/ShahGCreator/icon@main/PNG/909042007.png"},
    {"id": "909041002", "name": "رقصة الفرح", "img": "https://cdn.jsdelivr.net/gh/ShahGCreator/icon@main/PNG/909041002.png"},
    {"id": "909041003", "name": "رقصة النصر", "img": "https://cdn.jsdelivr.net/gh/ShahGCreator/icon@main/PNG/909041003.png"},
    {"id": "909041004", "name": "رقصة الهيب هوب", "img": "https://cdn.jsdelivr.net/gh/ShahGCreator/icon@main/PNG/909041004.png"},
    {"id": "909041005", "name": "رقصة الروك", "img": "https://cdn.jsdelivr.net/gh/ShahGCreator/icon@main/PNG/909041005.png"}
]

@app.route("/", methods=["GET", "POST"])
def index():
    results = []
    team_code = request.form.get("team_code", "")
    selected_emote_id = request.form.get("selected_emote", "")
    
    # جمع بيانات الـ IDs من الحقول الأربعة
    user_ids = []
    for i in range(1, 5):
        user_id = request.form.get(f"user_id_{i}", "").strip()
        if user_id:
            user_ids.append(user_id)
    
    if request.method == "POST" and team_code and selected_emote_id and user_ids:
        # إرسال رقصة واحدة لجميع اللاعبين في طلب واحد
        data = json.dumps({
            "teamcode": team_code,
            "emote_id": selected_emote_id,
            "target_ids": user_ids,  # جميع الـ IDs في قائمة واحدة
            "region": "ME"
        })
        
        try:
            res = requests.post("https://m2.0xarm.com/api/proxy_emote", 
                              headers=headers, cookies=cookies, data=data)
            
            # معالجة الرد
            response_text = res.text
            response_status = res.status_code
            
            # إضافة نتيجة واحدة للطلب الكامل
            results.append({
                "team_code": team_code,
                "emote_id": selected_emote_id,
                "user_ids": user_ids,
                "response": response_text,
                "status": response_status,
                "success": response_status == 200
            })
                    
        except Exception as e:
            results.append({
                "team_code": team_code,
                "emote_id": selected_emote_id,
                "user_ids": user_ids,
                "response": f"خطأ في الاتصال: {str(e)}",
                "status": "Error",
                "success": False
            })

    return render_template("index.html", 
                         emotes=emotes, 
                         results=results,
                         team_code=team_code,
                         selected_emote_id=selected_emote_id)

# هذه الدالة مهمة لـ Vercel
@app.route('/api/health')
def health():
    return jsonify({"status": "healthy"})

# هذه الدالة مهمة لـ Vercel
if __name__ == "__main__":
    app.run(debug=True, host='0.0.0.0', port=int(os.environ.get('PORT', 5000)))