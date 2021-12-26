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
$List = Get-ChildItem -LiteralPath $targetPath -Directory
ForEach ($Folder in $List) {
    $FolderSize = (Get-ChildItem -LiteralPath $Folder.FullName -Recurse -ErrorAction SilentlyContinue | Measure-Object -Property Length -Sum).sum

    switch ($FolderSize) {
    
        { ($FolderSize -ge 999) -and ($FolderSize -le 1000000) } {
            $NewFolderSize = $FolderSize / 1KB; 
            $NewFolderSize = [math]::round($NewFolderSize);
            $NewFolderSize = $NewFolderSize.ToString('000') + " KB";
            $FolderString = "(" + $NewFolderSize + ")";
        }
        { ($FolderSize -ge 999999) -and ($FolderSize -le 1000000000) } {
            $NewFolderSize = $FolderSize / 1MB; 
            $NewFolderSize = [math]::round($NewFolderSize);
            $NewFolderSize = $NewFolderSize.ToString('000') + " MB";
            $FolderString = "(" + $NewFolderSize + ")";
        }
        { ($FolderSize -ge 999999999) -and ($FolderSize -le 10000000000) } {
            #
            $NewFolderSize = $FolderSize / 1GB; 
            $NewFolderSize = [math]::round($NewFolderSize, 2);
            $NewFolderSize = $NewFolderSize.ToString('0.00') + " GB";
            $FolderString = "(" + $NewFolderSize + ")";
        }
        { ($FolderSize -ge 9999999999) -and ($FolderSize -le 1000000000000) } {
            $NewFolderSize = $FolderSize / 1GB; 
            $NewFolderSize = [math]::round($NewFolderSize, 1);
            $NewFolderSize = $NewFolderSize.ToString('00.0') + " GB";
            $FolderString = "(" + $NewFolderSize + ")";
        }
        { ($FolderSize -ge 999999999999) -and ($FolderSize -le 1000000000000000) } {
            $NewFolderSize = $FolderSize / 1TB; 
            $NewFolderSize = [math]::round($NewFolderSize);
            $NewFolderSize = $NewFolderSize.ToString('000') + " TB";
            $FolderString = "(" + $NewFolderSize + ")";
        }
        default { $NewFolderSize = "000 KB" }
    }
    
    $FolderString = "(" + $NewFolderSize + ")";
    $FolderName = "$Folder" + " " + $FolderString;

    if ($NewFolderSize -eq "000 KB") {
        Write-Host "This folder is empty: " $Folder;
    }
    else {
        Write-Host "This folder is being renamed to: " $FolderName;
        Rename-Item -LiteralPath $Folder.FullName $FolderName;
    }

}

Read-Host -Prompt "Completed. Press Enter to exit";