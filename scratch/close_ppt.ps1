try {
    $ppt = [System.Runtime.InteropServices.Marshal]::GetActiveObject('PowerPoint.Application')
    if ($ppt) {
        Write-Host "Found PowerPoint application. Closing..."
        $ppt.Quit()
        Write-Host "PowerPoint closed."
    }
} catch {
    Write-Host "COM get failed, checking process..."
    Stop-Process -Name POWERPNT -Force -ErrorAction SilentlyContinue
    Write-Host "PowerPoint process terminated."
}
Start-Sleep -Seconds 1
