let is_real_pest = false
basic.pause(1000)
basic.clearScreen()
// เชื่อมต่อกล้อง I2C และตั้งโหมดจำแนกวัตถุ (Object Classification)
huskylens.initI2c()
huskylens.initMode(protocolAlgorithm.OBJECTCLASSIFICATION)
// === 2. อ่านค่าและแสดงผลบนบอร์ดตัวเอง ===
basic.forever(function () {
    huskylens.request()
    // 1. ตรวจพบใบไม้สุขภาพดี (ID 1) -> แสดงรูปหัวใจและปิดพัดลม
    if (huskylens.isAppear(1, HUSKYLENSResultType_t.HUSKYLENSResultBlock)) {
        basic.showIcon(IconNames.Heart)
        pins.digitalWritePin(DigitalPin.P2, 0)
    } else if (huskylens.isAppear(2, HUSKYLENSResultType_t.HUSKYLENSResultBlock)) {
        // 2. ตรวจพบใบไม้มีปัญหา (ID 2) -> แสดงรูปหัวกะโหลกและปิดพัดลม
        basic.showIcon(IconNames.Skull)
        pins.digitalWritePin(DigitalPin.P2, 0)
    } else if (huskylens.isAppear(3, HUSKYLENSResultType_t.HUSKYLENSResultBlock) || huskylens.isAppear(4, HUSKYLENSResultType_t.HUSKYLENSResultBlock) || huskylens.isAppear(5, HUSKYLENSResultType_t.HUSKYLENSResultBlock)) {
        // 3. ตรวจพบแมลงศัตรูพืช (ID 3 = แมลงปอ, ID 4 = ผีเสื้อ, ID 5 = ตั๊กแตน)
        // --- เริ่มขั้นตอนการตรวจสอบความถูกต้องเชิงเวลา (Insect Verification - 5 วินาที) ---
        is_real_pest = true
        for (let index = 0; index < 5; index++) {
            // วนลูปตรวจสอบซ้ำ 5 ครั้ง ครั้งละ 1 วินาที (รวมเป็นเวลา 5 วินาที)
            basic.pause(1000)
            huskylens.request()
            // ถ้าในระหว่างช่วงเวลา 5 วินาทีนี้ แมลงหายไปจากเฟรมภาพแม้แต่วินาทีเดียว ให้ถือเป็นสัญญาณหลอก (False Alarm)
            if (!(huskylens.isAppear(3, HUSKYLENSResultType_t.HUSKYLENSResultBlock) || huskylens.isAppear(4, HUSKYLENSResultType_t.HUSKYLENSResultBlock) || huskylens.isAppear(5, HUSKYLENSResultType_t.HUSKYLENSResultBlock))) {
                is_real_pest = false
                break;
            }
        }
        // หลุดออกจากลูปตรวจเช็คทันที
        // หากผ่านการตรวจซ้ำแล้วพบว่าเป็นแมลงตัวเดิมค้างอยู่อย่างต่อเนื่องจนครบ 5 วินาทีจริง
        if (is_real_pest) {
            basic.showIcon(IconNames.Angry)
            // จ่ายสัญญาณ Analog ความแรง 100% (ค่า 1023) ไปสั่งหมุนมอเตอร์พัดลม P15
            pins.analogWritePin(AnalogPin.P2, 1023)
            // เปิดเป่าลมไล่แมลงค้างไว้เป็นเวลา 3 วินาที
            basic.pause(3000)
            // ปิดมอเตอร์พัดลมเมื่อทำงานเสร็จสิ้น
            pins.analogWritePin(AnalogPin.P2, 0)
        } else {
            // หากเป็นเพียงภาพสแกนแวบผ่านเข้ามาแล้วหายไป ให้เคลียร์จอและปิดพัดลม
            basic.clearScreen()
            pins.digitalWritePin(DigitalPin.P2, 0)
        }
    } else {
        // 4. กรณีสแกนไม่พบเป้าหมายที่เรียนรู้ใดๆ เลย
        basic.clearScreen()
        pins.digitalWritePin(DigitalPin.P2, 0)
    }
    basic.pause(100)
})
