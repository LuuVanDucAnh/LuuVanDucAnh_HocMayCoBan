try {
    $word = [System.Runtime.InteropServices.Marshal]::GetActiveObject('Word.Application')
    Write-Host "Found Word application. Active doc: $($word.ActiveDocument.Name)"
    $word.Quit(0)
    Write-Host "Word application closed successfully without saving unneeded temp changes."
} catch {
    Write-Host "Error or Word not running: $_"
}
