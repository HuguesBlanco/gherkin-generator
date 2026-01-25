# Google Gemini API Key Setup Guide

This guide walks you through creating a Google Gemini API key and setting up usage/budget limits to avoid surprise costs.

## Step 1: Create a Google Cloud Account

1. Go to [Google Cloud website](https://cloud.google.com)
2. Sign in with your Google account (or create one if needed)
   _A free trial is usually available_
3. Go to the [console](https://console.cloud.google.com)

## Step 2: Create a New Project (Optional but Recommended)

1. Click the project button at the top of the page
2. Click **"New Project"**
3. Enter a project name (e.g., "gherkin-generator")
4. Click **"Create"**
5. Select your new project

**Why create a project?** It helps you organize and track API usage separately from other Google Cloud services.

## Step 3: Enable the Gemini API

1. Go to **APIs & Services** → **API Library**
2. Search for **"Generative Language API"** (this is the official name for Gemini API)
3. Click on **"Generative Language API"**
4. Click **"Enable"**

## Step 4: Create an API Key

1. Go to **APIs & Services** → **Credentials** section
2. Click **"Create Credentials"** → **"API Key"**
3. In the popup:
   - Give your key a descriptive name (e.g., "Gemini API Key")
   - Under **"API restrictions"**, select **"Restrict key"** and choose **"Generative Language API"** only
   - Click **"Create"** (or **"Save"** if editing an existing key)
4. **Copy your API key** but keep it secret.

⚠️ **Important**: Don't share this key publicly or commit it to Git!

## Step 5: Set Usage/Budget Limits (CRITICAL)

### Option A: Set a Budget Alert (Recommended)

1. Go to **Billing** section
2. Select your billing account (or create one if needed)
3. Click **"Budgets & alerts"** in the left sidebar
4. Click **"Create Budget"**
5. Configure your budget:
   - **Budget name**: "General Monthly Limit" (or similar)
   - **Budget amount**: Set a safe limit (e.g., $5 or $10 for testing)
   - **Alert threshold**: Set to 50% and 90% (you'll get email alerts)
6. Click **"Create"**

⚠️ **Note**: If you select **"Savings"** as the budget type, be aware that it will deduct the free tier usage from your budget limit.

### Option B: Set Daily Quotas in the API

1. Go to **API & Services** → **Quotas**
2. Find **"Requests per day"** or **"Requests per minute"**
3. Click the quota you want to limit
4. Click **"Edit Quotas"**
5. Set a conservative limit (e.g., 100 requests per day for testing)
6. Click **"Submit"**

## Step 6: Verify Your Setup

1. Your API key should be visible in the **Credentials** section
2. Your budget alerts should be active in **Budgets & alerts** (if you created one)
3. You're ready to use the API key in the app!