$WshShell = New-Object -comObject WScript.Shell
$DesktopPath = [Environment]::GetFolderPath("Desktop")

# Remove existing shortcuts (including mangled ones via wildcard)
$ShortcutNames = @("Medya Atölyesi.lnk", "Medya Atolyesi.lnk", "MedyaIndirici - Kısayol.lnk", "Media Downloader.lnk", "Medya*lnk")
foreach ($name in $ShortcutNames) {
    $paths = Get-ChildItem -Path $DesktopPath -Filter $name -ErrorAction SilentlyContinue
    foreach ($p in $paths) {
        Remove-Item $p.FullName -Force
    }
}

# Clear icon cache (graceful attempt)
ie4uinit.exe -show

# Create new shortcut with pure ASCII name to avoid encoding issues
$ShortcutPath = Join-Path -Path $DesktopPath -ChildPath "Medya Atolyesi.lnk"
$Shortcut = $WshShell.CreateShortcut($ShortcutPath)
$Shortcut.TargetPath = "C:\Users\Burak\Desktop\url downloader\dist\MedyaIndirici\MedyaIndirici.exe"
$Shortcut.WorkingDirectory = "C:\Users\Burak\Desktop\url downloader\dist\MedyaIndirici"
# Point explicitly to the freshly generated icon2.ico file
$Shortcut.IconLocation = "C:\Users\Burak\Desktop\url downloader\icon3.ico"
$Shortcut.Save()

# Refresh Desktop
$code = @'
using System;
using System.Runtime.InteropServices;
public class IconRefresh {
    [DllImport("shell32.dll")]
    public static extern void SHChangeNotify(int wEventId, int uFlags, IntPtr dwItem1, IntPtr dwItem2);
    public static void Refresh() {
        SHChangeNotify(0x08000000, 0x0000, IntPtr.Zero, IntPtr.Zero);
    }
}
'@
Add-Type -TypeDefinition $code -ErrorAction SilentlyContinue
[IconRefresh]::Refresh()
