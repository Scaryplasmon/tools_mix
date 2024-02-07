$text = Get-Clipboard
$modifiedText = $text -replace '\\', '/'
Set-Clipboard -Value $modifiedText
