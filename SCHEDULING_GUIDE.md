# 📅 Scheduling Guide

Complete guide to using the scheduling features in Instagram Automation.

## 🎯 Overview

The scheduler allows you to:
- Schedule posts for specific future dates/times
- Create recurring daily/weekly/monthly posts
- Manage and cancel scheduled posts
- Auto-post while your computer is running

**Important**: Keep the application running in the background for scheduled posts to work!

---

## 📝 One-Time Scheduled Posts

### How to Schedule a Single Post:

1. **Open Scheduler**
   - Click "📅 Schedule Post for Later" button on Quick Post tab
   - OR click the "Scheduled Posts" tab and create new

2. **Select "One-Time Post"**
   - Choose specific date and time using calendar picker
   - Or use quick buttons:
     - "In 1 Hour" - Schedule 1 hour from now
     - "Tomorrow 9 AM" - Next day at 9:00 AM
     - "Next Week" - 7 days from now

3. **Choose Post Type**
   - Photo - For feed posts
   - Video/Reel - For video content
   - Story - For 24-hour stories

4. **Select Media File**
   - Click "Select File"
   - Choose your image or video

5. **Add Caption**
   - Write your caption
   - Add hashtags
   - Use emojis

6. **Schedule!**
   - Click "Schedule Post"
   - Post will auto-publish at scheduled time

### Example:
```
Schedule Type: One-Time
Date/Time: 2026-04-01 18:00
Post Type: Photo
Media: vacation_photo.jpg
Caption: Amazing sunset 🌅 #travel #sunset
```

---

## 🔄 Recurring Scheduled Posts

### How to Create Recurring Posts:

1. **Open Scheduler**
   - Click "📅 Schedule Post for Later"

2. **Select "Recurring Schedule"**

3. **Configure Schedule**
   - **Schedule Name**: Give it a memorable name (e.g., "Daily Motivation")
   - **Frequency**: Choose how often
     - **Daily**: Every day at specific time
     - **Weekly**: Same day each week
     - **Monthly**: Same date each month
     - **Yearly**: Same date each year

4. **Set Time and Date Options**
   - **Time of Day**: When to post (HH:MM format)
   - **Day of Week**: For weekly (Monday-Sunday)
   - **Day of Month**: For monthly (1-31)
   - **Month**: For yearly (January-December)

5. **Select Media Folder**
   - Choose a folder containing multiple images/videos
   - System will randomly pick one file each time
   - Supports: .jpg, .jpeg, .png, .mp4, .mov

6. **Add Caption Template**
   - Write a caption that works for all posts
   - Use generic hashtags

7. **Create Schedule**
   - Posts will automatically publish according to schedule
   - Continues until you disable it

### Example - Daily Posts:
```
Schedule Name: Daily Quote
Frequency: Daily
Time: 09:00
Media Folder: C:\Pictures\Quotes\
Caption: Daily inspiration 💡 #motivation #quotes
Result: Posts one random image from folder every day at 9 AM
```

### Example - Weekly Posts:
```
Schedule Name: Weekend Vibes
Frequency: Weekly
Day: Saturday
Time: 12:00
Media Folder: C:\Pictures\Weekend\
Caption: Weekend vibes ✨ #weekend #relax
Result: Posts every Saturday at noon
```

### Example - Monthly Posts:
```
Schedule Name: Monthly Update
Frequency: Monthly
Day of Month: 1
Time: 10:00
Media Folder: C:\Pictures\Updates\
Caption: New month, new goals! 🎯 #monthlyupdate
Result: Posts on the 1st of every month at 10 AM
```

---

## 📊 Managing Scheduled Posts

### View Scheduled Posts:

1. Go to "📅 Scheduled Posts" tab
2. See list of all scheduled posts:
   - Post ID
   - Type (photo/video/story)
   - Caption preview
   - Scheduled time
   - Status

### Cancel a Scheduled Post:

1. Select the post in the table
2. Click "❌ Cancel Selected"
3. Confirm cancellation
4. Post will not be published

### Refresh List:

- Click "🔄 Refresh" button
- Auto-refreshes every 30 seconds

---

## ⚙️ How the Scheduler Works

### Background Service
- Uses APScheduler (Python scheduling library)
- Runs in background while app is open
- Stores schedule in SQLite database
- Automatically retries failed posts

### Requirements
- **Application must be running** for posts to publish
- Computer should be on at scheduled time
- Instagram login must be active
- Media files must still exist at scheduled time

### What Happens at Scheduled Time:
1. Scheduler checks database
2. Loads media file
3. Logs into Instagram (using saved session)
4. Posts content with caption
5. Updates post status to "posted"
6. Logs result in database

### If Something Goes Wrong:
- Post marked as "failed"
- Error message saved
- Check logs for details: `logs/app_YYYYMMDD.log`
- You can reschedule manually

---

## 💡 Tips & Best Practices

### For Best Results:

✅ **DO**:
- Keep application running in background
- Test with one schedule first
- Use high-quality images
- Keep captions within Instagram limits (2200 chars)
- Schedule at least 5 minutes in future
- Organize media in folders for recurring posts

❌ **DON'T**:
- Schedule too many posts too close together
- Delete media files after scheduling
- Schedule past dates
- Post too frequently (Instagram may flag)
- Use copyrighted content

### Recommended Schedule Frequency:
- **Optimal**: 1-3 posts per day
- **Maximum**: 5 posts per day
- **Recurring**: Space at least 4 hours apart

### Best Times to Post (General):
- Morning: 6 AM - 9 AM
- Lunch: 12 PM - 1 PM
- Evening: 5 PM - 7 PM
- Night: 8 PM - 11 PM

*(Adjust based on your audience timezone)*

---

## 🔧 Troubleshooting

### Post didn't publish?

**Check:**
1. Application was running at scheduled time?
2. Instagram login still active?
3. Media file still exists at original location?
4. Internet connection working?
5. Check "Scheduled Posts" tab for error status

**Solutions:**
- Restart application
- Re-login to Instagram
- Reschedule the post
- Check logs folder for details

### Recurring posts not working?

**Check:**
1. Media folder path is correct?
2. Folder contains valid image/video files?
3. Schedule is active (not cancelled)?
4. Application running in background?

**Solutions:**
- Verify folder path
- Add more media files to folder
- Recreate the schedule
- Check schedule in database

---

## 📁 Database Location

Schedules stored in: `data/instagram_automation.db`

**Backup your database** to save schedules:
```
Copy: data/instagram_automation.db
To: [your backup location]
```

---

## 🚨 Important Notes

⚠️ **Instagram Rate Limits**:
- Don't post more than 5 times per day
- Space posts at least 30 minutes apart
- Avoid spam-like behavior

⚠️ **Application Requirements**:
- Must stay running for schedules to work
- Session persists between restarts
- Logs all activity for debugging

⚠️ **Responsibility**:
- Follow Instagram's Terms of Service
- Don't spam or violate community guidelines
- Use for your own account only
- Respect copyright on media

---

**Need Help?** Check the logs in `logs/` folder or refer to the main README.md

**Made with ❤️ for the Instagram community**
