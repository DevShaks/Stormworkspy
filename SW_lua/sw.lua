-- Constants
API_PORT = 5000
API_ENDPOINT = '/'

-- Initial Variables
tick_interval = 10
is_reply_pending = true

http_response_body = ''
http_request_body = ''

-- Tables to hold the received values
receivedNums = {}
receivedBools = {}

-- Main Tick Function
function onTick()
    tick_interval = tick_interval - 1

    if tick_interval < 1 and is_reply_pending then
        tick_interval = 5
        transmit()
    end

    for i = 1, 32 do
        output.setNumber(i, receivedNums[i] or 0)
    end
    
    for i = 1, 32 do
        -- Convert true/false to 1/0
        output.setNumber(i + 32, receivedBools[i] and 1 or 0)
    end
    
end

-- Transmit function: Encodes 32 numerical and 32 boolean values into a GET request.
function transmit()
    local query = "?"
    -- Append 32 numerical values
    for i = 1, 32 do
        local value = input.getNumber(i)
        query = query .. "num" .. i .. "=" .. value .. "&"
    end
    -- Append 32 boolean values
    for i = 1, 32 do
        local boolVal = input.getBool(i)
        query = query .. "bool" .. i .. "=" .. tostring(boolVal) .. "&"
    end
    -- Remove the trailing '&'
    query = string.sub(query, 1, -2)

    async.httpGet(API_PORT, API_ENDPOINT .. query)
    is_reply_pending = false
end

-- HTTP Reply Function: Decodes the response into 32 numerical and 32 boolean values.
function httpReply(port, request_body, response_body)
    http_response_body = response_body
    http_request_body = request_body

    local data = jsonDecode(response_body)
    if data then
        -- Extract numerical values
        for i = 1, 32 do
            receivedNums[i] = tonumber(data["num" .. i])
        end
        -- Extract boolean values (assuming the JSON returns "true"/"false" as strings)
        for i = 1, 32 do
            local val = data["bool" .. i]
            receivedBools[i] = (val == "true")
        end
    else
        -- You can set an error message or default values if needed
        http_response_body = "Invalid JSON response"
    end

    is_reply_pending = true
end

-- Custom JSON Decode Function
function jsonDecode(json_string)
    local json = {}
    local key, value
    json_string = json_string:gsub('"%s*:', '":')
    json_string = json_string:gsub(',%s*"', ',"')
    json_string = json_string:gsub(':%s*"', ': "')
    json_string = json_string:gsub(',%s*}', '}')
    json_string = json_string:gsub('{%s*"', '{"')
    
    for k, v in json_string:gmatch('"(.-)":%s*(.-)[,%}]') do
        key = k:gsub('%s*$', '')
        value = v:gsub('^%s*', ''):gsub('%s*$', ''):gsub('^"', ''):gsub('"$', '')
        json[key] = value
    end
    return json
end

-- Draw Function: Displays the HTTP response (for debugging)
function onDraw()
    width = screen.getWidth()
	height = screen.getHeight()

    screen.drawTextBox(1, 1, width, height, http_response_body, 0, 0)
end
