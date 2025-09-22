import asyncio
from mavsdk import System
from mavsdk.offboard import OffboardError, PositionNedYaw

async def gradual_ascent(drone, target_altitude, step=1.0, delay=2):
    """Kademeli yükseliş fonksiyonu"""
    current = 0.0
    while current > -target_altitude:
        current -= step
        print(f"⬆️ Going up: {abs(current):.1f} m")
        await drone.offboard.set_position_ned(PositionNedYaw(0.0, 0.0, current, 0.0))
        await asyncio.sleep(delay)

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

    # 1. ADIM: 5 metreye kademeli çık
    await gradual_ascent(drone, target_altitude=5.0, step=1.0, delay=2)

    # 2. ADIM: Havada 5 sn kal
    print("⏳ Holding position...")
    await asyncio.sleep(5)

    # 3. ADIM: Kademeli iniş
    current = -5.0
    while current < 0.0:
        current += 1.0
        print(f"⬇️ Going down: {abs(current):.1f} m left")
        await drone.offboard.set_position_ned(PositionNedYaw(0.0, 0.0, current, 0.0))
        await asyncio.sleep(2)

    # 4. ADIM: Offboard durdur ve inişi garantile
    print("🛑 Stopping offboard...")
    try:
        await drone.offboard.stop()
    except OffboardError as e:
        print(f"❌ Offboard stop failed: {e._result.result}")

    print("🛬 Landing (safety)...")
    await drone.action.land()

    # İnişi tamamla
    async for in_air in drone.telemetry.in_air():
        if not in_air:
            print("✅ Landed")
            break

    print("⛔ Disarming...")
    await drone.action.disarm()

if __name__ == "__main__":
    asyncio.run(run())
