import asyncio
import cv2
import numpy as np
from mavsdk import System
from mavsdk.offboard import OffboardError, PositionNedYaw, VelocityNedYaw

async def run():
    # Drone bağlantısı
    drone = System()
    await drone.connect(system_address="udp://:14540")

    print("🔌 Connecting...")
    async for state in drone.core.connection_state():
        if state.is_connected:
            print("✅ Connected to drone")
            break

    print("⚡ Arming...")
    await drone.action.arm()

    print("🚁 Starting offboard...")
    try:
        await drone.offboard.set_position_ned(PositionNedYaw(0.0, 0.0, 0.0, 0.0))
        await drone.offboard.start()
    except OffboardError as e:
        print(f"❌ Offboard start failed: {e._result.result}")
        await drone.action.disarm()
        return

    # Offboard ile kalkış (3m yukarı)
    print("⬆️ Takeoff to 3m (offboard)")
    await drone.offboard.set_position_ned(PositionNedYaw(0.0, 0.0, -3.0, 0.0))
    await asyncio.sleep(5)

    # OpenCV kamera
    cap = cv2.VideoCapture(0)
    frame_center_x = int(cap.get(3) / 2)

    try:
        while True:
            ret, frame = cap.read()
            if not ret:
                break

            hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)

            # Yeşil renk aralığı
            lower_green = np.array([40, 40, 40])
            upper_green = np.array([80, 255, 255])
            mask = cv2.inRange(hsv, lower_green, upper_green)

            contours, _ = cv2.findContours(mask, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)

            command = "HOVER"
            vx, vy = 0.0, 0.0
            vz = 0.0  # irtifa sabit

            if contours:
                cnt = max(contours, key=cv2.contourArea)
                area = cv2.contourArea(cnt)
                if area > 500:
                    x, y, w, h = cv2.boundingRect(cnt)
                    obj_center_x = x + w // 2

                    cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 2)

                    if obj_center_x < frame_center_x - 50:
                        command = "LEFT"
                        vy = -1.0
                    elif obj_center_x > frame_center_x + 50:
                        command = "RIGHT"
                        vy = 1.0
                    else:
                        command = "FORWARD"
                        vx = 1.0

            # Drone velocity komutu
            await drone.offboard.set_velocity_ned(VelocityNedYaw(vx, vy, vz, 0.0))

            cv2.putText(frame, f"CMD: {command}", (30, 30),
                        cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)
            cv2.imshow("Frame", frame)
            cv2.imshow("Mask", mask)

            if cv2.waitKey(1) & 0xFF == ord('q'):
                break

    finally:
        cap.release()
        cv2.destroyAllWindows()
        print("🛬 Landing...")
        await drone.action.land()
        async for in_air in drone.telemetry.in_air():
            if not in_air:
                break
        await drone.action.disarm()

if __name__ == "__main__":
    asyncio.run(run())

