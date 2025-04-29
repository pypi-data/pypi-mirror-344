import asyncio
import subprocess
import platform
import speedtest
from rich.console import Console
from rich.panel import Panel
from rich.table import Table
from rich.live import Live

# Run shell commands safely
def run_command(cmd):
    try:
        return subprocess.check_output(cmd, shell=True).decode().strip()
    except subprocess.CalledProcessError:
        return "<command failed>"

# Asynchronously ping a host
async def ping_host(host):
    cmd = f"ping -c 1 {host}" if platform.system() != "Windows" else f"ping -n 1 {host}"
    process = await asyncio.create_subprocess_shell(cmd, stdout=asyncio.subprocess.PIPE, stderr=asyncio.subprocess.PIPE)
    stdout, _ = await process.communicate()
    return stdout.decode().strip()

# Asynchronously get download and upload speeds
async def get_speed():
    try:
        st = speedtest.Speedtest()
        st.get_best_server()
        download_speed = st.download() / 1_000_000
        upload_speed = st.upload() / 1_000_000
        return round(download_speed, 2), round(upload_speed, 2)
    except Exception:
        return 0.0, 0.0

# Asynchronously run traceroute
async def traceroute(host):
    cmd = f"traceroute {host}" if platform.system() != "Windows" else f"tracert {host}"
    process = await asyncio.create_subprocess_shell(cmd, stdout=asyncio.subprocess.PIPE, stderr=asyncio.subprocess.PIPE)
    stdout, _ = await process.communicate()
    return stdout.decode().strip()

# Build a rich table for UI display
def build_table(ping_result, trace_result, download_speed, upload_speed):
    table = Table(title="NetCrackr Live Monitor", expand=True)
    table.add_column("Component", style="bold cyan")
    table.add_column("Status", style="green")

    ping_line = ping_result.split('\n')[0] if ping_result else "Failed"
    trace_line = trace_result.split('\n')[1] if trace_result and len(trace_result.split('\n')) > 1 else "N/A"

    table.add_row("📶 Ping to google.com", ping_line)
    table.add_row("⬇ Download Speed", f"{download_speed} Mbps")
    table.add_row("⬆ Upload Speed", f"{upload_speed} Mbps")
    table.add_row("🧭 Traceroute (1st hop)", trace_line)

    return table

# Continuously run the monitor
async def live_trace_and_speed():
    console = Console()
    target = "google.com"

    with Live(console=console, refresh_per_second=1) as live:
        while True:
            try:
                # Run all tests concurrently
                ping_task = asyncio.create_task(ping_host(target))
                trace_task = asyncio.create_task(traceroute(target))
                speed_task = asyncio.create_task(get_speed())

                ping_result, trace_result, (download_speed, upload_speed) = await asyncio.gather(
                    ping_task, trace_task, speed_task
                )

                table = build_table(ping_result, trace_result, download_speed, upload_speed)
                live.update(Panel(table, title="[bold magenta]🧠 NetCrackr LIVE TRACE[/bold magenta]", border_style="magenta"))

            except Exception as e:
                live.update(Panel(f"[bold red]Error:[/bold red] {e}", title="⚠ NetCrackr Crash", border_style="red"))

            await asyncio.sleep(10)  # Wait before next update

# CLI function
def cli():
    try:
        asyncio.run(live_trace_and_speed())
    except KeyboardInterrupt:
        print("\n[!] NetCrackr stopped by user. Goodbye!")

# Entrypoint
if __name__ == "__main__":
    cli()
