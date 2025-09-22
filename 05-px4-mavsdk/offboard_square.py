import asyncio
from mavsdk import System
from mavsdk.offboard import OffboardError, PositionNedYaw

async def run():
    drone = System()
    await drone.connect(system_address="udp://:14540")

    print("🔌 Connecting...")
    async for state in drone.core.connection_state():
        if state.is_connected:
            print("✅ Connected")
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

    # Kalk: 3 metre yukarı
    print("⬆️ Taking off to 3m")
    await drone.offboard.set_position_ned(PositionNedYaw(0.0, 0.0, -3.0, 0.0))
    await asyncio.sleep(5)

    # 1. ileri (x=5m)
    print("➡️ Forward 5m")
    await drone.offboard.set_position_ned(PositionNedYaw(5.0, 0.0, -3.0, 0.0))
    await asyncio.sleep(5)

    # 2. sağa (y=5m)
    print("➡️ Right 5m")
    await drone.offboard.set_position_ned(PositionNedYaw(5.0, 5.0, -3.0, 0.0))
    await asyncio.sleep(5)

    # 3. geri (x=0)
    print("⬅️ Backward")
    await drone.offboard.set_position_ned(PositionNedYaw(0.0, 5.0, -3.0, 0.0))
    await asyncio.sleep(5)

    # 4. sola (y=0)
    print("⬅️ Left")
    await drone.offboard.set_position_ned(PositionNedYaw(0.0, 0.0, -3.0, 0.0))
    await asyncio.sleep(5)

    # İniş
    print("🛬 Landing...")
    await drone.offboard.stop()
    await drone.action.land()

    async for in_air in drone.telemetry.in_air():
        if not in_air:
            print("✅ Landed")
            break

    print("⛔ Disarming...")
    await drone.action.disarm()

if __name__ == "__main__":
    asyncio.run(run())

