--[[ 
    Roblox Studio RPC Plugin
    Author: PrayoadMii
--]]

local HttpService = game:GetService("HttpService")
local Players = game:GetService("Players")
local ServerURL = "http://127.0.0.1:1234/StudioRPC/Update"

local toolbar = plugin:CreateToolbar("Studio RPC (Client)")
local ToggleButton = toolbar:CreateButton(
	"Studio RPC (Client)",
	"Check Did You're Running Server Or Not If Icon Is Red",
	"rbxassetid://132676871546283"
)

local Status = "Plugin Is Starting..."

local function GetThumbnailsFromId(Id:number)
	local url = ("https://thumbnails.roproxy.com/v1/users/avatar-headshot?userIds=%d&size=100x100&format=Png&isCircular=true"):format(Id)
	local success, response = pcall(function()
		return HttpService:GetAsync(url)
	end)
	if success then
		local data = HttpService:JSONDecode(response)
		return data.data[1].imageUrl
	else
		return nil
	end
end

local function GetPlaceThumbnail(placeId:number)
	local url = ("https://thumbnails.roproxy.com/v1/places/gameicons?placeIds=%d&size=150x150&format=Png"):format(placeId)
	local success, response = pcall(function()
		return HttpService:GetAsync(url)
	end)
	if success then
		local data = HttpService:JSONDecode(response)
		if data and data.data and data.data[1] then
			return data.data[1].imageUrl
		end
	end
	return nil
end

local function GetGameName() :string
	local susess, resault = pcall(function()
		return game:GetService("MarketplaceService"):GetProductInfo(game.PlaceId)
	end)
	if susess then
		return resault.Name
	else
		return game.Name
	end
end

local function SendRPCToServerAsync(Line1, Line2, BigImage, BigImageTip, SmallImage, SmallImageTip)
	local DataToSendToServer = {
		Details = Line1 or nil,
		State = Line2 or nil,
		LargeImage = BigImage or nil,
		SmallImage = SmallImage or nil,
		BigImageToolHover = BigImageTip or "Roblox Studio",
		SmallImageHover = SmallImageTip or "Editing As: nil"
	}
	local success, err = pcall(function()
		HttpService:PostAsync(ServerURL, HttpService:JSONEncode(DataToSendToServer), Enum.HttpContentType.ApplicationJson)
	end)
	if not success then
		ToggleButton.Icon = "rbxassetid://117554232976059"
		Status = "Cannot Sonnect To Server! Check Is Server Is Running Or Not Or Download It At https://prayoadmii.neocities.org/Creations/RobloxStudioRPC"
	else
		ToggleButton.Icon = "rbxassetid://117636057142584"
		Status = "Server Was Connected!"
	end
end

local function GetItem()
	local selected = game:GetService("Selection"):Get()
	if #selected > 1 then
		return selected[1].Name .. " And Others " .. #selected .. " Instances"
	elseif #selected > 0 then
		return selected[1].Name
	else
		return "Nothing"
	end
end

ToggleButton.Click:Connect(function()
	print("[Studio RPC]: " .. Status)
end)

task.spawn(function()
	while task.wait(2.5) do
		local player = Players.LocalPlayer
		if player then
			local avatarUrl = GetThumbnailsFromId(player.UserId)
			SendRPCToServerAsync(
				GetGameName(),
				GetItem(),
				GetPlaceThumbnail(game.PlaceId),
				GetGameName(),
				avatarUrl,
				"Editing As: " .. player.DisplayName
			)
		end
	end
end)