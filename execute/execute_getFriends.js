var targets = Args.targets;
var friends = {};
var req;
var itr = 0;
var lst = targets.split(",");

// из строки с целями вынимаем каждую цель
while (itr <= lst.length) {
	// сразу делаем запросы, как только вытащили id
	req = API.friends.get({ "user_id": lst[itr], "fields": "city,photo" });
	
	if (req) {
		friends = friends + [req];
	} else {
		friends = friends + [0];
	}

    itr = itr + 1;
}

return friends;