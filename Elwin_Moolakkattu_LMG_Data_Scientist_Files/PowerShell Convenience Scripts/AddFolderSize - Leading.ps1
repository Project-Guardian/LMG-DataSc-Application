$targetPath = Read-Host -Prompt "Enter path"
Write-Host "---------------------------------------------------------------------";

$List = Get-ChildItem -LiteralPath $targetPath -Directory
ForEach ($Folder in $List) {
    if ($Folder -like '(* *B *) *') {    #'* (* *B)'
        $Matching = $Folder `
        -ireplace '\([0-3] B [a-zA-Z_0-9][a-zA-Z_0-9][a-zA-Z_0-9]\)', "" `
        -ireplace '\([0-3] [A-Z]B [a-zA-Z_0-9][a-zA-Z_0-9][a-zA-Z_0-9]\)', "" `
        -ireplace '\([0-9] [A-Z]B [a-zA-Z_0-9][.][a-zA-Z_0-9][a-zA-Z_0-9]\)', "" `
        -ireplace '\([0-9] [A-Z]B [a-zA-Z_0-9][a-zA-Z_0-9][.][a-zA-Z_0-9]\)', "" `
        -ireplace '\([0-9] [A-Z]B [a-zA-Z_0-9][a-zA-Z_0-9][a-zA-Z_0-9][.]\)', "";
        Write-Host "This folder already has the size and will be rechecked: " $Folder;
        Rename-Item -LiteralPath $Folder.FullName $Matching.Trim();
    }
}

Write-Host "---------------------------------------------------------------------";
$List = Get-ChildItem -LiteralPath $targetPath -Directory
ForEach ($Folder in $List) {
    $FolderSize = (Get-ChildItem -LiteralPath $Folder.FullName -Recurse -ErrorAction SilentlyContinue | Measure-Object -Property Length -Sum).sum

    switch ($FolderSize) {
        
        { ($FolderSize -ge 0) -and ($FolderSize -le 1000) } {
            $NewFolderSize = $FolderSize; 
            $NewFolderSize = [math]::round($NewFolderSize);
            $NewFolderSize = "1 B " + $NewFolderSize.ToString('000');
            $FolderString = "(" + $NewFolderSize + ")";
        }
        { ($FolderSize -ge 999) -and ($FolderSize -le 1000000) } {
            $NewFolderSize = $FolderSize / 1KB; 
            $NewFolderSize = [math]::round($NewFolderSize);
            $NewFolderSize = "2 KB " + $NewFolderSize.ToString('000');
            $FolderString = "(" + $NewFolderSize + ")";
        }
        { ($FolderSize -ge 999999) -and ($FolderSize -le 1000000000) } {
            $NewFolderSize = $FolderSize / 1MB; 
            $NewFolderSize = [math]::round($NewFolderSize);
            $NewFolderSize = "3 MB " + $NewFolderSize.ToString('000');
            $FolderString = "(" + $NewFolderSize + ")";
        }
        { ($FolderSize -ge 999999999) -and ($FolderSize -le 10000000000) } {
            #
            $NewFolderSize = $FolderSize / 1GB; 
            $NewFolderSize = [math]::round($NewFolderSize, 2);
            $NewFolderSize = "4 GB " + $NewFolderSize.ToString('0.00');
            $FolderString = "(" + $NewFolderSize + ")";
        }
        { ($FolderSize -ge 9999999999) -and ($FolderSize -le 1000000000000) } {
            $NewFolderSize = $FolderSize / 1GB; 
            $NewFolderSize = [math]::round($NewFolderSize, 1);
            $NewFolderSize = "4 GB " + $NewFolderSize.ToString('00.0');
            $FolderString = "(" + $NewFolderSize + ")";
        }
        { ($FolderSize -ge 999999999999) -and ($FolderSize -le 1000000000000000) } {
            $NewFolderSize = $FolderSize / 1TB; 
            $NewFolderSize = [math]::round($NewFolderSize);
            $NewFolderSize = "5 TB " + $NewFolderSize.ToString('000');
            $FolderString = "(" + $NewFolderSize + ")";
        }
        default { $NewFolderSize = "(0 KB 000)" }
    }
    
    $FolderString = "(" + $NewFolderSize + ")";
    $FolderName = $FolderString + " " + "$Folder"; # 

    if ($NewFolderSize -eq "(0 KB 000)") {
        Write-Host "This folder is empty: " $Folder;
    }
    else {
        Write-Host "This folder is being renamed to: " $FolderName;
        Rename-Item -LiteralPath $Folder.FullName $FolderName;
    }

}

Read-Host -Prompt "Completed. Press Enter to exit";