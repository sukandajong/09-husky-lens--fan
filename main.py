is_real_pest = False
basic.pause(1000)
basic.clear_screen()
# เชื่อมต่อกล้อง I2C และตั้งโหมดจำแนกวัตถุ (Object Classification)
huskylens.init_i2c()
huskylens.init_mode(protocolAlgorithm.OBJECTCLASSIFICATION)
# === 2. อ่านค่าและแสดงผลบนบอร์ดตัวเอง ===

def on_forever():
    global is_real_pest
    huskylens.request()
    # 1. ตรวจพบใบไม้สุขภาพดี (ID 1) -> แสดงรูปหัวใจและปิดพัดลม
    if huskylens.is_appear(1, HUSKYLENSResultType_t.HUSKYLENS_RESULT_BLOCK):
        basic.show_icon(IconNames.HEART)
        pins.digital_write_pin(DigitalPin.P2, 0)
    elif huskylens.is_appear(2, HUSKYLENSResultType_t.HUSKYLENS_RESULT_BLOCK):
        # 2. ตรวจพบใบไม้มีปัญหา (ID 2) -> แสดงรูปหัวกะโหลกและปิดพัดลม
        basic.show_icon(IconNames.SKULL)
        pins.digital_write_pin(DigitalPin.P2, 0)
    elif huskylens.is_appear(3, HUSKYLENSResultType_t.HUSKYLENS_RESULT_BLOCK) or huskylens.is_appear(4, HUSKYLENSResultType_t.HUSKYLENS_RESULT_BLOCK) or huskylens.is_appear(5, HUSKYLENSResultType_t.HUSKYLENS_RESULT_BLOCK):
        # 3. ตรวจพบแมลงศัตรูพืช (ID 3 = แมลงปอ, ID 4 = ผีเสื้อ, ID 5 = ตั๊กแตน)
        # --- เริ่มขั้นตอนการตรวจสอบความถูกต้องเชิงเวลา (Insect Verification - 5 วินาที) ---
        is_real_pest = True
        for index in range(5):
            # วนลูปตรวจสอบซ้ำ 5 ครั้ง ครั้งละ 1 วินาที (รวมเป็นเวลา 5 วินาที)
            basic.pause(1000)
            huskylens.request()
            # ถ้าในระหว่างช่วงเวลา 5 วินาทีนี้ แมลงหายไปจากเฟรมภาพแม้แต่วินาทีเดียว ให้ถือเป็นสัญญาณหลอก (False Alarm)
            if not (huskylens.is_appear(3, HUSKYLENSResultType_t.HUSKYLENS_RESULT_BLOCK) or huskylens.is_appear(4, HUSKYLENSResultType_t.HUSKYLENS_RESULT_BLOCK) or huskylens.is_appear(5, HUSKYLENSResultType_t.HUSKYLENS_RESULT_BLOCK)):
                is_real_pest = False
                break
        # หลุดออกจากลูปตรวจเช็คทันที
        # หากผ่านการตรวจซ้ำแล้วพบว่าเป็นแมลงตัวเดิมค้างอยู่อย่างต่อเนื่องจนครบ 5 วินาทีจริง
        if is_real_pest:
            basic.show_icon(IconNames.ANGRY)
            # จ่ายสัญญาณ Analog ความแรง 100% (ค่า 1023) ไปสั่งหมุนมอเตอร์พัดลม P15
            pins.analog_write_pin(AnalogPin.P2, 1023)
            # เปิดเป่าลมไล่แมลงค้างไว้เป็นเวลา 3 วินาที
            basic.pause(3000)
            # ปิดมอเตอร์พัดลมเมื่อทำงานเสร็จสิ้น
            pins.analog_write_pin(AnalogPin.P2, 0)
        else:
            # หากเป็นเพียงภาพสแกนแวบผ่านเข้ามาแล้วหายไป ให้เคลียร์จอและปิดพัดลม
            basic.clear_screen()
            pins.digital_write_pin(DigitalPin.P2, 0)
    else:
        # 4. กรณีสแกนไม่พบเป้าหมายที่เรียนรู้ใดๆ เลย
        basic.clear_screen()
        pins.digital_write_pin(DigitalPin.P2, 0)
    basic.pause(100)
basic.forever(on_forever)
