def track(arr, cnt = 8):
	if len(arr) == cnt:
		print arr
		return
	for i in range(cnt):
		if i in arr:
			continue
		available = True
		for j in range(len(arr)):
			if abs(arr[j] - i) == len(arr) - j:
				available = False
				break
		if not available:
			continue
		track(arr + [i], cnt)
	return

track([], cnt = 40)
