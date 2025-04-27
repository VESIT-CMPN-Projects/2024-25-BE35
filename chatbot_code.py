import streamlit as st
import speech_recognition as sr
import datetime
from datetime import datetime
#and the access its now method simpler
d1 = datetime.now()
# Set page configuration
st.set_page_config(
    page_title="Mental Health Support Assistant",
    page_icon="🤖",
    layout="centered"
)

# Initialize session state
if 'conversation_history' not in st.session_state:
    st.session_state.conversation_history = []
if 'last_topic' not in st.session_state:
    st.session_state.last_topic = None

# Custom CSS with improved design and animations
st.markdown("""
<style>
    /* Main background with gradient */
    .main {
        background: linear-gradient(135deg, #f0f4ff 0%, #e6f0fa 100%);
        position: relative;
        overflow: hidden;
    }
     .main::before {
        content: '';
        position: absolute;
        width: 100%;
        height: 100%;
        background: inherit;
        z-index: 0;
    }
    
    /* Header styling */
    h1 {
        background: linear-gradient(90deg, #4568dc, #b06ab3);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        font-size: 2.5rem !important;
        margin-bottom: 0.5rem !important;
        text-align: center;
    }
    
    /* Subheader styling */
    .subheader {
        text-align: center;
        color: #555;
        margin-bottom: 2rem;
        font-style: italic;
    }
    
     /* Wave animation background */
    .wave-container {
        position: fixed;
        width: 100%;
        height: 100%;
        top: 0;
        left: 0;
        z-index: 0;
        pointer-events: none;
        overflow: hidden;
    }
    
    .wave {
        position: absolute;
        width: 200%;
        height: 200%;
        top: -50%;
        left: -50%;
        border-radius: 40%;
        animation: wave 20s infinite linear;
        opacity: 0.1;
    }
    
    .wave:nth-child(1) {
        background: radial-gradient(ellipse at center, #4568dc 0%, transparent 70%);
        animation-duration: 25s;
    }
    
    .wave:nth-child(2) {
        background: radial-gradient(ellipse at center, #b06ab3 0%, transparent 70%);
        animation-duration: 30s;
        animation-delay: -5s;
    }
    
    .wave:nth-child(3) {
        background: radial-gradient(ellipse at center, #4facfe 0%, transparent 70%);
        animation-duration: 35s;
        animation-delay: -10s;
    }
    
    @keyframes wave {
        0% {
            transform: rotate(0deg);
        }
        100% {
            transform: rotate(360deg);
        }
    }
    
    /* Floating particles */
    .particle {
        position: absolute;
        width: 8px;
        height: 8px;
        border-radius: 50%;
        opacity: 0.4;
        pointer-events: none;
        animation: float 15s infinite ease-in-out;
    }
    
    .particle:nth-child(1) {
        background: #4568dc;
        left: 10%;
        top: 20%;
        animation-duration: 18s;
    }
    
    .particle:nth-child(2) {
        background: #b06ab3;
        left: 30%;
        top: 50%;
        animation-duration: 22s;
        animation-delay: 2s;
    }
    
    .particle:nth-child(3) {
        background: #4facfe;
        left: 50%;
        top: 30%;
        animation-duration: 20s;
        animation-delay: 4s;
    }
    
    .particle:nth-child(4) {
        background: #6a11cb;
        left: 70%;
        top: 60%;
        animation-duration: 25s;
        animation-delay: 1s;
    }
    
    .particle:nth-child(5) {
        background: #2575fc;
        left: 90%;
        top: 40%;
        animation-duration: 19s;
        animation-delay: 3s;
    }
    
    @keyframes float {
        0%, 100% {
            transform: translateY(0) translateX(0);
        }
        25% {
            transform: translateY(-30px) translateX(15px);
        }
        50% {
            transform: translateY(-15px) translateX(-15px);
        }
        75% {
            transform: translateY(-45px) translateX(10px);
        }
    }
    
    # /* Chat container */
    # .chat-container {
    #     background: rgba(255, 255, 255, 0.8);
    #     border-radius: 12px;
    #     padding: 1rem;
    #     margin-bottom: 1rem;
    #     box-shadow: 0 4px 6px rgba(0, 0, 0, 0.05);
    #     max-height: 60vh;
    #     overflow-y: auto;
    # }
    
    /* Chat message styling */
    .chat-message { 
        padding: 1rem; 
        border-radius: 12px; 
        margin-bottom: 1rem; 
        display: flex; 
        position: relative; 
        z-index: 2; 
        box-shadow: 0 2px 5px rgba(0, 0, 0, 0.05);
        animation: fadeIn 0.5s ease-in-out;
    }
    
    @keyframes fadeIn {
        from { opacity: 0; transform: translateY(10px); }
        to { opacity: 1; transform: translateY(0); }
    }
    
    .chat-message.user { 
        background: linear-gradient(135deg, #6e8efb, #a777e3); 
        color: #fff; 
        margin-left: 2rem;
        margin-right: 0.5rem;
    }
    
    .chat-message.bot { 
        background: linear-gradient(135deg, #8e9eab, #eef2f3); 
        color: #333; 
        margin-right: 2rem;
        margin-left: 0.5rem;
    }
    
    .chat-message .avatar {
        width: 40px;
        height: 40px;
        border-radius: 50%;
        display: flex;
        align-items: center;
        justify-content: center;
        margin-right: 10px;
        font-size: 20px;
    }
    
    .chat-message .message { 
        flex: 1;
        line-height: 1.5;
    }
    
    .chat-message .timestamp {
        font-size: 0.7rem;
        opacity: 0.7;
        margin-top: 5px;
        text-align: right;
    }
    
    # /* Input area styling */
    # .input-area {
    #     background: rgba(255, 255, 255, 0.9);
    #     border-radius: 12px;
    #     padding: 1rem;
    #     box-shadow: 0 4px 6px rgba(0, 0, 0, 0.05);
    #     margin-top: 1rem;
    # }
    
    /* Button styling */
    .stButton > button {
        background: linear-gradient(90deg, #4568dc, #b06ab3);
        color: white;
        border: none;
        border-radius: 50px;
        padding: 0.5rem 1.5rem;
        font-weight: bold;
        transition: all 0.3s ease;
    }
    
    .stButton > button:hover {
        transform: translateY(-2px);
        box-shadow: 0 4px 8px rgba(0, 0, 0, 0.1);
    }
    
    /* Form styling */
    .input-container {
        display: flex;
        align-items: center;
    }
    
    /* Resources section */
    .resources {
        background: rgba(255, 255, 255, 0.8);
        border-radius: 12px;
        padding: 1rem;
        margin-top: 1rem;
        box-shadow: 0 4px 6px rgba(0, 0, 0, 0.05);
    }
    
    /* Disclaimer */
    .disclaimer {
        text-align: center;
        font-size: 0.8rem;
        color: #777;
        margin-top: 2rem;
    }
    
    /* Make the app container wider */
    .stApp {
        max-width: 1000px;
        margin: 0 auto;
    }
    
    /* Custom text input */
    .stTextInput > div > div > input {
        border-radius: 50px;
        padding-left: 1rem;
        border: 1px solid #ddd;
    }
    
    /* Custom form submit button */
    .stFormSubmitButton > button {
        border-radius: 50px;
        background: linear-gradient(90deg, #4568dc, #b06ab3);
        color: white;
    }
    
    /* Expander styling */
    .streamlit-expanderHeader {
        background: rgba(255, 255, 255, 0.8);
        border-radius: 8px;
        padding: 0.5rem;
        font-weight: bold;
        color: #555;
    }
    
    /* Topic pills */
    .topic-pills {
        display: flex;
        flex-wrap: wrap;
        gap: 8px;
        margin: 1rem 0;
        justify-content: center;
    }
    
    .topic-pill {
        background: linear-gradient(90deg, #4568dc, #b06ab3);
        color: white;
        padding: 5px 15px;
        border-radius: 50px;
        font-size: 0.9rem;
        cursor: pointer;
        transition: all 0.3s ease;
        display: inline-block;
    }
    
    .topic-pill:hover {
        transform: translateY(-2px);
        box-shadow: 0 4px 8px rgba(0, 0, 0, 0.1);
    }
</style>
<div class="wave-container">
    <div class="wave"></div>
    <div class="wave"></div>
    <div class="wave"></div>
</div>
<div class="particle"></div>
<div class="particle"></div>
<div class="particle"></div>
<div class="particle"></div>
<div class="particle"></div>
""", unsafe_allow_html=True)

# Title and introduction
st.markdown("<div style='display: flex; align-items: center;'><span style='font-size: 2.5rem; margin-right: 10px;'>👨🏻‍💻</span><h1>Mental Health Support Assistant</h1></div>", unsafe_allow_html=True)
st.markdown("<p class='subheader' style='font-weight: bold;font-size: 16px'>Your companion for mental wellness - ask anything and get personalized guidance</p>", unsafe_allow_html=True)

# Quick topic selection pills
st.markdown("<div class='topic-pills'>"+
            "<span class='topic-pill'>😰 Anxiety</span>"+
            "<span class='topic-pill'>😔 Depression</span>"+
            "<span class='topic-pill'>😫 Stress</span>"+
            "<span class='topic-pill'>😴 Sleep</span>"+
            "<span class='topic-pill'>🧘 Self-Care</span>"+
            "<span class='topic-pill'>📱 Screen Time</span>"+
            "</div>", unsafe_allow_html=True)


# Mental health knowledge base
mental_health_knowledge = {
    "anxiety": {
        "description": "Anxiety is a natural stress response involving excessive worry or fear about future events.",
        "causes": ["High stress", "Trauma", "Genetics", "Caffeine or substance use", "Unresolved conflicts"],
        "symptoms": ["Persistent worry", "Restlessness", "Rapid heartbeat", "Trouble focusing", "Sleep issues"],
        "immediate_coping": ["Deep breathing (4-7-8)", "Grounding (5-4-3-2-1 senses)", "Cold water splash on face", "Short walk"],
        "long_term_management": ["Mindfulness practice", "Regular exercise (30 min/day)", "Therapy (CBT)", "Healthy diet", "Sleep routine"],
        "cautions": ["Avoid overthinking triggers", "Limit overstimulation", "Maintain routine", "Stay hydrated", "Seek early support"],
        "professional_help": ["CBT therapy", "SSRIs or anti-anxiety meds", "Support groups", "Psychiatrist consultation"]
    },
    "depression": {
        "description": "Depression is a mood disorder causing persistent sadness and loss of interest.",
        "causes": ["Loss or trauma", "Chemical imbalances", "Chronic stress", "Isolation", "Family history"],
        "symptoms": ["Ongoing sadness", "Fatigue", "Sleep changes", "Appetite shifts", "Hopelessness"],
        "immediate_coping": ["Talk to someone", "Get sunlight", "Do a small task", "Listen to uplifting music"],
        "long_term_management": ["Set achievable goals", "Exercise regularly", "Therapy (CBT/IP)", "Social connection", "Nutrition focus"],
        "cautions": ["Avoid isolation", "Limit alcohol", "Stick to routines", "Monitor negative thoughts", "Seek help early"],
        "professional_help": ["Psychotherapy (CBT)", "Antidepressants", "TMS or ECT for severe cases", "Counseling"]
    },
    "stress": {
        "description": "Stress is the body’s reaction to pressure, impacting health when chronic.",
        "causes": ["Work demands", "Life changes", "Financial issues", "Lack of rest", "Overcommitment"],
        "symptoms": ["Irritability", "Headaches", "Poor concentration", "Sleep problems", "Muscle tension"],
        "immediate_coping": ["Deep breathing", "Step away briefly", "Drink water", "Stretch or move"],
        "long_term_management": ["Time management", "Regular physical activity", "Mindfulness or yoga", "Set boundaries", "Creative outlets"],
        "cautions": ["Avoid overloading tasks", "Limit screen time", "Ensure rest", "Stay connected", "Address early signs"],
        "professional_help": ["Stress coaching", "MBSR programs", "Biofeedback", "Therapist for burnout"]
    },
    "sleep": {
        "description": "Sleep is crucial for mental health, aiding mood and cognitive function.",
        "causes_of_issues": ["Stress or anxiety", "Screen time", "Caffeine late in day", "Irregular schedule", "Medical conditions"],
        "symptoms_of_issues": ["Difficulty falling asleep", "Frequent waking", "Daytime fatigue", "Irritability"],
        "immediate_coping": ["Relaxing music", "Dark room", "Warm tea (no caffeine)", "Body scan meditation"],
        "long_term_management": ["Consistent sleep schedule", "Bedtime routine", "No screens 1-2 hrs before", "Limit caffeine", "CBT-I"],
        "cautions": ["Avoid late naps", "Limit heavy meals at night", "Reduce evening stress", "Maintain dark room"]
    },
    "crisis": {
        "description": "A mental health crisis involves immediate risk to self or others.",
        "causes": ["Overwhelming despair", "Trauma", "Substance use", "Loss of support"],
        "warning_signs": ["Suicidal thoughts", "Hopelessness", "Reckless behavior", "Extreme mood swings"],
        "immediate_resources": ["Call 988 (Suicide Lifeline)", "Text HOME to 741741", "911 for emergencies", "Trevor Project: 1-866-488-7386"],
        "long_term_management": ["Ongoing therapy", "Build a support network", "Develop coping skills", "Regular mental health check-ins"]
    },
    "self_care": {
        "description": "Self-care involves intentional actions to maintain physical, emotional, and mental well-being.",
        "types": ["Physical (exercise, sleep)", "Emotional (journaling, therapy)", "Social (connecting with others)", "Mental (learning, hobbies)"],
        "immediate_coping": ["Take a 5-min break", "Hydrate", "Step outside", "Positive self-talk"],
        "long_term_management": ["Daily movement", "Balanced diet", "Regular check-ins with self", "Set personal goals"]
    },
    "screen_time": {
        "description": "Screen time refers to time spent on digital devices, impacting mental and physical health.",
        "bad_effects": ["Eye strain", "Poor sleep quality", "Increased stress or anxiety", "Reduced focus", "Social isolation"],
        "reduction_strategies": ["Set screen time limits (e.g., 1-2 hrs/day)", "Use blue light filters", "Take breaks every 30 min", "Replace screen time with hobbies", "No screens 1 hr before bed"],
        "age_recommendations": ["Ages 5-10: 1 hr/day supervised", "Ages 11-15: 2 hrs/day with breaks", "Balance with physical activity and sleep"],
        "immediate_coping": ["Turn off devices for 10 min", "Step outside", "Blink frequently to rest eyes", "Stretch your body"],
        "long_term_management": ["Establish screen-free zones (e.g., bedroom)", "Schedule device-free days", "Promote offline hobbies", "Monitor usage with apps"]
    }
}

# Optimized response function with context
def get_response(query):
    query = query.lower().strip()
    
    # Crisis detection - highest priority
    crisis_keywords = {"suicide", "kill myself", "end my life", "harm myself", "crisis", "emergency", 
                      "want to die", "no reason to live", "hurt myself", "self harm", "cutting myself"}
    if any(kw in query for kw in crisis_keywords):
        info = mental_health_knowledge["crisis"]
        st.session_state.last_topic = "crisis"
        return f"**Immediate Support Needed**:\n\n1. 🚨 {info['description']}\n\n2. 📞 Resources:\n   - {info['immediate_resources'][0]}\n   - {info['immediate_resources'][1]}\n   - {info['immediate_resources'][2]}\n\n3. 💡 Reach out now—your safety matters!"

    
    # Check for age-specific screen time questions
    age_pattern = r'\b(\d+)[\s-]*(?:year|yr)s?[\s-]*old\b'
    import re
    age_match = re.search(age_pattern, query)
    
    if ("screen time" in query or "screen" in query or "device" in query or "phone" in query) and age_match:
        age = int(age_match.group(1))
        topic = "screen_time"
        st.session_state.last_topic = topic
        
        # Age-specific recommendations
        if 5 <= age <= 10:
            return "📱 **Screen Time for 5 to 10 Year-Old Children**:\n\n1. 🕒 **Recommended limit**: 1 hour per day of high-quality content\n\n2. 👀 **Always supervised**: Adult supervision is essential\n\n3. 🎮 **Content matters**: Educational and age-appropriate content only\n\n4. 🌿 **Balance**: Ensure plenty of physical play, reading, and social interaction\n\n5. 💤 **No screens**: At least 1 hour before bedtime to avoid sleep disruption\n\n6. 🍎 **Screen-free zones**: Keep mealtimes and bedrooms screen-free"
        elif 11 <= age <= 15:
            return "📱 **Screen Time for 11-15 Year Olds**:\n\n1. 🕒 **Recommended limit**: 2 hours per day of recreational screen time\n\n2. ⏰ **Regular breaks**: 10-minute break every 30 minutes\n\n3. 🏃 **Physical activity**: At least 1 hour of physical activity daily to balance screen time\n\n4. 🛌 **No screens**: At least 1 hour before bedtime\n\n5. 🔍 **Monitoring**: Parents should be aware of content being consumed\n\n6. 📵 **Screen-free times**: Establish daily screen-free periods for family time"
        else:
            # For ages outside our specific ranges
            return "📱 **Screen Time Recommendations**:\n\n1. The American Academy of Pediatrics recommends:\n   - Ages 0-18 months: No screen time except video chatting\n   - Ages 18-24 months: Limited high-quality programming with adult interaction\n   - Ages 2-5: 1 hour per day of high-quality content\n   - Ages 6+: Consistent limits on time and content\n\n2. 🔄 **Balance is key**: Screen time should not replace physical activity, sleep, or other essential health behaviors\n\n3. 👨‍👩‍👧‍👦 **Family media plan**: Create a personalized plan at healthychildren.org/MediaUsePlan"

    # Enhanced topic detection with expanded keywords
    topic_keywords = {
        "anxiety": {"anxiety", "anxious", "worry", "panic", "nervous", "fearful", "fear", "phobia", 
                   "scared", "tense", "on edge", "uneasy", "dread", "apprehension", "jittery"},
        "depression": {"depression", "depressed", "sad", "hopeless", "down", "low", "blue", "miserable", 
                      "unhappy", "melancholy", "despair", "worthless", "empty", "numb", "unmotivated"},
        "stress": {"stress", "stressed", "overwhelm", "burnout", "pressure", "tension", "strain", 
                  "overload", "busy", "hectic", "frazzled", "exhausted", "drained"},
        "sleep": {"sleep", "insomnia", "tired", "rest", "awake", "fatigue", "drowsy", "bed", "nap", 
                 "nightmares", "snoring", "sleepy", "exhausted", "can't sleep", "wake up"},
        "self_care": {"self-care", "self care", "wellness", "balance", "me time", "self-love", 
                     "self-compassion", "mindfulness", "relaxation", "recharge", "boundaries"},
        "screen_time": {"screen time", "phone use", "device", "screen", "digital", "social media", 
                       "internet", "computer", "smartphone", "tablet", "gaming", "online", "tech"}
    }
    
    # More comprehensive intent detection
    intent_keywords = {
        "causes": {"why", "cause", "reason", "triggers", "source", "origin", "where from", "lead to", "result in"},
        "symptoms": {"symptoms", "signs", "feel like", "what happens", "experience", "notice", "tell if", "identify", "recognize"},
        "immediate_coping": {"now", "quick", "fast", "immediately", "right away", "what if", "doesn't work", "can't", 
                            "urgent", "emergency", "help me", "struggling", "this moment", "tonight"},
        "long_term_management": {"long term", "over time", "manage", "cope", "deal with", "daily", "keep up", 
                                "routine", "habit", "practice", "maintain", "sustain", "ongoing"},
        "cautions": {"cautions", "prevent", "avoid", "watch out", "worse", "danger", "risk", "harmful", 
                    "negative", "careful", "warning", "look out for"},
        "professional_help": {"professional", "therapy", "doctor", "treatment", "help", "therapist", 
                             "counselor", "psychiatrist", "medication", "specialist", "clinic"},
        "types": {"types", "kinds", "options", "varieties", "different", "categories", "forms", "examples"},
        "bad_effects": {"bad effects", "negative", "harm", "problem", "damage", "consequences", "impact", "hurt"},
        "reduction_strategies": {"reduce", "cut down", "less", "limit", "decrease", "minimize", "lower", "control"},
        "age_recommendations": {"age", "kids", "children", "teens", "how much", "young", "adolescent", "youth", "parent"}
    }

    # Expanded scenario recognition
    scenarios = {
        "overwhelmed at work": ("stress", "🌟 **Feeling Overwhelmed at Work? Try This**:\n\n1. ⏰ Break tasks into small, manageable chunks.\n\n2. 🌿 Take 5-min breaks to breathe deeply.\n\n3. 🗣️ Discuss workload with a supervisor.\n\n4. 🛌 Prioritize rest to avoid burnout."),
        "can't sleep because of stress": ("sleep", "🌙 **Can't Sleep Due to Stress? Here's Help**:\n\n1. 🧘 Do a 5-min meditation to relax.\n\n2. 📴 No screens 1 hr before bed.\n\n3. ✍️ Write down worries to clear your mind.\n\n4. ☕ Avoid caffeine after midday."),
        "feeling worthless": ("depression", "💙 **Feeling Worthless? You're Enough**:\n\n1. 🌞 Get 10 min of sunlight or fresh air.\n\n2. 🎯 Complete one small task (e.g., make your bed).\n\n3. 🤝 Call a friend or family member.\n\n4. 🌿 Say: 'My worth isn't my productivity.'"),
        "panic before exams": ("anxiety", "📚 **Panic Before Exams? Stay Calm**:\n\n1. 🌬️ Use 4-7-8 breathing to steady yourself.\n\n2. ✏️ Study one topic at a time.\n\n3. 🏃 Walk for 5 min to reset.\n\n4. 💬 Affirm: 'I've done my best.'"),
        "no energy to do anything": ("depression", "⚡ **No Energy? Start Small**:\n\n1. 💧 Drink water to hydrate.\n\n2. 🌞 Sit by a window or step outside.\n\n3. 🎶 Play a favorite song.\n\n4. 🌱 Set a tiny goal (e.g., stand up for 1 min)."),
        "too much on my mind": ("stress", "🧠 **Too Much on Your Mind? Unload It**:\n\n1. ✍️ Write a quick list of thoughts.\n\n2. 🌿 Breathe deeply for 1 min.\n\n3. ⏰ Focus on one thing for 10 min.\n\n4. 🗣️ Talk it out with someone."),
        "how to start self-care": ("self_care", "🌈 **Starting Self-Care? Easy Steps**:\n\n1. 🚶 Move your body for 5 min.\n\n2. 💧 Sip water mindfully.\n\n3. 📝 Note one thing you're grateful for.\n\n4. 🌿 Plan 10 min of 'me time' today."),
        "too much screen time": ("screen_time", "📱 **Too Much Screen Time? Here's Help**:\n\n1. ⏳ Set a timer for 1-2 hrs/day.\n\n2. 🌐 Use blue light filters.\n\n3. 🕒 Take a 5-min break every 30 min.\n\n4. 🎨 Swap screens for a hobby."),
        "always worried": ("anxiety", "🌈 **Always Worried? Try These Techniques**:\n\n1. 📝 Write down your worries to externalize them.\n\n2. 🔍 Ask: 'What's the evidence for and against this worry?'\n\n3. ⏱️ Set a 15-min 'worry time' each day.\n\n4. 🧠 Practice thought-stopping by saying 'STOP' when worries begin."),
        "social anxiety": ("anxiety", "👥 **Social Anxiety Relief**:\n\n1. 🌱 Start with small, brief social interactions.\n\n2. 👁️ Focus outward instead of on yourself.\n\n3. 🧘 Practice deep breathing before social events.\n\n4. 🔄 Challenge negative thoughts with realistic alternatives."),
        "grief and loss": ("depression", "💔 **Coping with Grief and Loss**:\n\n1. 🕊️ Allow yourself to feel without judgment.\n\n2. 📔 Express feelings through writing or art.\n\n3. 🤝 Connect with others who understand.\n\n4. 🌱 Honor your loved one in meaningful ways."),
        "procrastination": ("stress", "⏰ **Overcoming Procrastination**:\n\n1. 🍅 Try the Pomodoro technique (25 min work, 5 min break).\n\n2. 🥇 Start with the easiest task to build momentum.\n\n3. 🧩 Break large tasks into smaller steps.\n\n4. 🎯 Set specific, achievable goals with deadlines."),
        "phone addiction": ("screen_time", "📱 **Breaking Phone Addiction**:\n\n1. 🔕 Turn off non-essential notifications.\n\n2. ⏰ Set specific times to check your phone.\n\n3. 🌙 Use grayscale mode to reduce visual appeal.\n\n4. 🔄 Replace phone habits with alternative activities."),
        "trouble focusing": ("stress", "🔍 **Improving Focus and Concentration**:\n\n1. 🧹 Clear physical and digital clutter.\n\n2. 📝 Use a to-do list to externalize tasks.\n\n3. 🔇 Find a quiet space or use white noise.\n\n4. ⏱️ Work in focused 25-minute intervals with breaks.")
    }

    # Advanced topic detection with partial matching
    topic = None
    max_scenario_match = 0
    matched_scenario = None
    
    # Check for scenario matches with partial matching
    for scenario, (scen_topic, response) in scenarios.items():
        # Calculate what percentage of the scenario words appear in the query
        scenario_words = set(scenario.split())
        query_words = set(query.split())
        common_words = scenario_words.intersection(query_words)
        
        if len(scenario_words) > 0:
            match_percentage = len(common_words) / len(scenario_words)
            if match_percentage > 0.7 and match_percentage > max_scenario_match:  # 70% threshold
                max_scenario_match = match_percentage
                matched_scenario = scenario
    
    if matched_scenario:
        topic, response = scenarios[matched_scenario]
        st.session_state.last_topic = topic
        return response
    
    # Check for topic keywords
    for t, keywords in topic_keywords.items():
        if any(kw in query for kw in keywords):
            topic = t
            st.session_state.last_topic = topic
            break
    
    # Use context from previous conversation if no topic detected
    if not topic and st.session_state.last_topic:
        topic = st.session_state.last_topic
    
    # If still no topic, provide a helpful default response
    if not topic:
        return "🤔 I'm here to help with mental health questions! You can ask about:\n\n1. 😰 **Anxiety** - Worry, panic, nervousness\n2. 😔 **Depression** - Sadness, low mood, lack of motivation\n3. 😫 **Stress** - Feeling overwhelmed, burnout\n4. 😴 **Sleep** - Insomnia, fatigue, better rest\n5. 🧘 **Self-care** - Wellness practices, balance\n6. 📱 **Screen time** - Digital habits, reducing usage\n\nOr describe a situation like 'I'm feeling overwhelmed at work' or 'I can't sleep because of stress'."

    info = mental_health_knowledge[topic]

    # Enhanced intent detection with fuzzy matching
    intent = None
    max_intent_match = 0
    
    for i, keywords in intent_keywords.items():
        for kw in keywords:
            if kw in query:
                # Simple word count for relevance
                relevance = len(kw.split())
                if relevance > max_intent_match:
                    max_intent_match = relevance
                    intent = i
    
    # Default to most helpful intent if none detected
    if not intent:
        if "how" in query or "what" in query or "ways" in query:
            intent = "immediate_coping"
        else:
            intent = "long_term_management"

    # Comprehensive response mapping
    intent_responses = {
        "causes": (f"🔍 **Causes of {topic.capitalize()}**:", info.get("causes", info.get("causes_of_issues", []))),
        "symptoms": (f"🚩 **Signs of {topic.capitalize()}**:", info.get("symptoms", info.get("symptoms_of_issues", []))),
        "immediate_coping": (f"⏳ **Quick Help for {topic.capitalize()}**:", info.get("immediate_coping", [])),
        "long_term_management": (f"🌱 **Managing {topic.capitalize()} Long-Term**:", info.get("long_term_management", [])),
        "cautions": (f"🛡️ **Cautions for {topic.capitalize()}**:", info.get("cautions", [])),
        "professional_help": (f"🩺 **Professional Help for {topic.capitalize()}**:", info.get("professional_help", [])),
        "types": (f"🌟 **Types of {topic.capitalize()}**:", info.get("types", [])),
        "bad_effects": (f"⚠️ **Negative Effects of {topic.capitalize()}**:", info.get("bad_effects", [])),
        "reduction_strategies": (f"📴 **How to Reduce {topic.capitalize()}**:", info.get("reduction_strategies", [])),
        "age_recommendations": (f"⏰ **Age-Appropriate Guidelines for {topic.capitalize()}**:", info.get("age_recommendations", []))
    }

    title, items = intent_responses.get(intent, intent_responses["long_term_management"])
    
    # Handle empty responses gracefully
    if not items:
        # Try to find alternative information to provide
        for alt_intent in ["immediate_coping", "long_term_management", "symptoms"]:
            alt_title, alt_items = intent_responses.get(alt_intent, (None, []))
            if alt_items:
                return f"{title}\n\nI don't have specific information on that aspect, but here's related guidance:\n\n" + "\n\n".join(f"{i+1}. {item}" for i, item in enumerate(alt_items))
        
        # If still no information, provide a general response
        return f"I don't have specific information about {intent.replace('_', ' ')} for {topic}, but I can help with other aspects. Try asking about symptoms, coping strategies, or long-term management."
    
    # Format response with emoji bullets for better readability
    emoji_bullets = ["🔹", "🔸", "💠", "🔷", "🔶"]
    formatted_items = "\n\n".join(f"{emoji_bullets[i % len(emoji_bullets)]} {item}" for i, item in enumerate(items))
    
    # Add a helpful tip or follow-up suggestion based on the topic and intent
    follow_up_suggestions = {
        "anxiety": "💡 **Tip**: Anxiety often responds well to breathing exercises and cognitive restructuring.",
        "depression": "💡 **Tip**: Regular physical activity can be as effective as medication for mild depression.",
        "stress": "💡 **Tip**: Setting boundaries and learning to say 'no' are crucial stress management skills.",
        "sleep": "💡 **Tip**: Consistency is key—try to go to bed and wake up at the same time every day.",
        "self_care": "💡 **Tip**: Even 5 minutes of self-care daily can make a significant difference.",
        "screen_time": "💡 **Tip**: The quality of screen time matters as much as the quantity."
    }
    
    tip = follow_up_suggestions.get(topic, "")
    
    return f"{title}\n\n{formatted_items}\n\n{tip}"
# Audio recording function
def record_audio():
    r = sr.Recognizer()
    with sr.Microphone() as source:
        st.write("🎤 Listening... Speak your question")
        audio = r.listen(source)
        try:
            return r.recognize_google(audio)
        except sr.UnknownValueError:
            return "Sorry, I couldn’t understand the audio."
        except sr.RequestError:
            return "Network error—please try typing instead."

# Display conversation history with improved styling
st.markdown("<div class='chat-container'>", unsafe_allow_html=True)
if not st.session_state.conversation_history:
    st.markdown("<p style='text-align: center;color: rgb(44 36 36);padding: 2rem;font-weight: bold;'>Start a conversation by typing a question below or selecting a topic above.</p>", unsafe_allow_html=True)
else:
    for message in st.session_state.conversation_history:
        role_class = "user" if message["role"] == "user" else "bot"
        emoji = "👤" if message["role"] == "user" else "🧠"
        timestamp = message.get("timestamp", d1.strftime("%I:%M %p"))
        
        st.markdown(f"""
        <div class="chat-message {role_class}">
            <div class="avatar">{emoji}</div>
            <div class="message-container">
                <div class="message">{message['content']}</div>
                <div class="timestamp">{timestamp}</div>
            </div>
        </div>
        """, unsafe_allow_html=True)
st.markdown("</div>", unsafe_allow_html=True)

# Input section with improved styling
st.markdown("<div class='input-area'>", unsafe_allow_html=True)
col1, col2 = st.columns([5, 1])

with col1:
    with st.form(key="text_form", clear_on_submit=True):
        user_query = st.text_input("", placeholder="Ask me anything about mental health...", label_visibility="collapsed")
        submit_button = st.form_submit_button(label="Send")
        if submit_button and user_query:
            st.session_state.conversation_history.append({
                "role": "user", 
                "content": user_query,
                "timestamp": d1.strftime("%I:%M %p")
            })
            response = get_response(user_query)
            st.session_state.conversation_history.append({
                "role": "bot", 
                "content": response,
                "timestamp": d1.strftime("%I:%M %p")
            })
            st.rerun()

with col2:
    if st.button("🎤"):
        user_query = record_audio()
        if user_query and not user_query.startswith("Sorry") and not user_query.startswith("Network"):
            st.session_state.conversation_history.append({
                "role": "user", 
                "content": user_query,
                "timestamp": d1.strftime("%I:%M %p")
            })
            response = get_response(user_query)
            st.session_state.conversation_history.append({
                "role": "bot", 
                "content": response,
                "timestamp": d1.strftime("%I:%M %p")
            })
            st.rerun()

# Action buttons
col1, col2 = st.columns(2)
with col1:
    if st.session_state.conversation_history and st.button("🗑️ Clear Chat"):
        st.session_state.conversation_history = []
        st.session_state.last_topic = None
        st.rerun()
with col2:
    if st.session_state.conversation_history and st.button("📋 Save Chat"):
        chat_text = "\n\n".join([f"{'You' if msg['role'] == 'user' else 'Assistant'}: {msg['content']}" for msg in st.session_state.conversation_history])
        st.download_button(
            label="Download Conversation",
            data=chat_text,
            file_name=f"mental_health_chat_{d1.strftime('%Y%m%d_%H%M%S')}.txt",
            mime="text/plain",
            key="download_chat"
        )
st.markdown("</div>", unsafe_allow_html=True)

# Resources with improved styling
with st.expander("📚 Additional Resources"):
    st.markdown("""
    <div style="display: grid; grid-template-columns: 1fr 1fr; gap: 20px;">
        <div>
            <h4>Crisis Helplines</h4>
            <ul>
                <li><strong>Global:</strong> 988 (Suicide Lifeline, US) | Text HOME to 741741 (Crisis Text Line, US)</li>
                <li><strong>Vandrevala Foundation:</strong> 9999 666 555 (24/7 support across India)</li>
                <li><strong>Sneha India:</strong> 044-24640050 (Chennai-based, 24/7)</li>
                <li><strong>AASRA:</strong> 9820466726 (Mumbai-based, 24/7)</li>
                <li><strong>iCall (TISS):</strong> 9152987821 (Mon-Sat, 8 AM - 10 PM)</li>
            </ul>
        </div>
        <div>
            <h4>Organizations</h4>
            <ul>
                <li><strong>Global:</strong> <a href="https://www.nami.org" target="_blank">NAMI</a> | <a href="https://www.mhanational.org" target="_blank">Mental Health America</a></li>
                <li><strong>Sangath:</strong> <a href="https://www.sangath.in" target="_blank">www.sangath.in</a> - Community-based programs</li>
                <li><strong>Live Love Laugh:</strong> <a href="https://www.thelivelovelaughfoundation.org" target="_blank">www.thelivelovelaughfoundation.org</a></li>
                <li><strong>Mpower:</strong> <a href="https://www.mpowerminds.com" target="_blank">www.mpowerminds.com</a> - Services across India</li>
                <li><strong>White Swan Foundation:</strong> <a href="https://www.whiteswanfoundation.org" target="_blank">www.whiteswanfoundation.org</a></li>
            </ul>
        </div>
    </div>
    <div style="margin-top: 15px;">
        <h4>Self-Help Resources</h4>
        <ul>
            <li><a href="https://www.mindful.org" target="_blank">Mindfulness Resources</a> - Guided practices and articles</li>
            <li><a href="https://www.nimhans.ac.in/departments/nimhans-centre-for-well-being" target="_blank">NIMHANS Well-being Resources</a> - Tools from India's National Institute</li>
            <li><a href="https://www.headspace.com" target="_blank">Headspace</a> - Meditation and mindfulness app</li>
            <li><a href="https://www.calm.com" target="_blank">Calm</a> - Sleep, meditation and relaxation app</li>
        </ul>
    </div>
    """, unsafe_allow_html=True)

