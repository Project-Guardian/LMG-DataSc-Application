$targetPath = Read-Host -Prompt "Enter path"
Write-Host "---------------------------------------------------------------------";

$List = Get-ChildItem -LiteralPath $targetPath -Directory
ForEach ($Folder in $List) {
    if ($Folder -like '* (* *B)') {    
        $Matching = $Folder `
        -ireplace ' \([a-zA-Z_0-9][a-zA-Z_0-9][a-zA-Z_0-9] [A-Z]B\)', "" `
        -ireplace ' \([a-zA-Z_0-9][.][a-zA-Z_0-9][a-zA-Z_0-9] [A-Z]B\)', "" `
        -ireplace ' \([a-zA-Z_0-9][a-zA-Z_0-9][.][a-zA-Z_0-9] [A-Z]B\)', "" `
        -ireplace ' \([a-zA-Z_0-9][a-zA-Z_0-9][a-zA-Z_0-9][.][a-zA-Z_0-9] [A-Z]B\)', "";
        Write-Host "This folder already has the size and will be rechecked: " $Folder;
        Rename-Item -LiteralPath $Folder.FullName $Matching;
    }
}
Write-Host "---------------------------------------------------------------------";
Write-Host "Finished removing folder sizes";

Read-Host -Prompt "Completed. Press Enter to exit";