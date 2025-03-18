$event = "SELECT * FROM __InstanceCreationEvent WITHIN 5 WHERE TargetInstance ISA 'Win32_NTLogEvent' AND (TargetInstance.EventCode = '4647' OR TargetInstance.EventCode = '4634')"
Register-WmiEvent -Query $event -Action {
	Write-Host '[+] User logged out or session terminated. Running malware...'
}
