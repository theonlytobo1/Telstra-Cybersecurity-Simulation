# www.theforage.com - Telstra Cyber Task 3
# Test Requester

import http.client

host = "localhost"
port = 8000

def main():
    target = "%s:%s" % (host, port)
    print("[+] Beginning test requests to: %s" % target)
    successful_responses = 0

    for x in range(0, 5):
        payload = "class.module.classLoader.resources.context.parent.pipeline.first.pattern=%25%7Bc2%7Di..."
        print("[%s/5]: Making test request to %s with payload: %s" % (x + 1, target, payload))
        conn = http.client.HTTPConnection(target)

        conn.request('POST', '/tomcatwar.jsp', payload,  {
            "suffix": "%>//",
            "c1": "Runtime",
            "c2": "<%",
            "DNT": "1",
            "Content-Type": "application/x-www-form-urlencoded",
        })
        response = conn.getresponse()
        status_code = response.status
        if status_code == 200:
            successful_responses += 1
        print("Response status code: %s" % status_code)
        print("=============")

    print("[+] Test completed.")
    print("[+] Successful responses: %s/5" % successful_responses)

if __name__ == "__main__":
    main()
