import streamlit as st
import pandas as pd
from sklearn.linear_model import LinearRegression

st.title("❄️ حاسبة الحمل الحراري")
st.write("أدخل بيانات غرفتك، والموقع يحسب حجم المكيف المناسب بطريقتين: الحساب التقليدي وتوقع مبني على بيانات طقس حقيقية")
st.write("برمجة: المهندس محمد")

def cooling_load(wall_area, temp_difference, num_people, num_equipment):
    wall_heat = wall_area * 2.5 * temp_difference
    people_heat = num_people * 100
    equipment_heat = num_equipment * 60
    total_load_watts = wall_heat + people_heat + equipment_heat
    total_load_tons = total_load_watts / 3517
    return total_load_watts, total_load_tons

df = pd.read_csv("weatherHistory.csv")
X = df[["Humidity"]]
y = df["Temperature (C)"]
model = LinearRegression()
model.fit(X, y)

st.subheader("📐 بيانات الغرفة")
room_length = st.number_input("طول الغرفة (م)", value=5.0)
room_width = st.number_input("عرض الغرفة (م)", value=4.0)

ceiling_height = 2.5
perimeter = (room_length + room_width) * 2
wall_area = perimeter * ceiling_height
st.write("مساحة الجدران المحسوبة تلقائياً:", round(wall_area, 1), "م²")

st.subheader("👥 بيانات الاستخدام")
num_people = st.number_input("عدد الأشخاص", value=2)
num_equipment = st.number_input("عدد الأجهزة (اختياري)", value=0)
humidity = st.slider("نسبة الرطوبة", 0.0, 1.0, 0.70)

if st.button("احسب"):
    predicted_temp = model.predict([[humidity]])[0]
    watts_ai, tons_ai = cooling_load(wall_area, predicted_temp, num_people, num_equipment)
    
    available_sizes = [1, 1.5, 2, 2.5, 3, 4, 5]
    recommended_size = available_sizes[-1]
    for size in available_sizes:
        if size >= tons_ai:
            recommended_size = size
            break
    
    st.subheader("🌡️ النتيجة")
    st.metric("المقاس الموصى به", f"{recommended_size} طن تبريد")
    st.caption(f"مبني على حساب حراري مع بيانات طقس حقيقية (الحمل الدقيق: {round(tons_ai, 2)} طن)")