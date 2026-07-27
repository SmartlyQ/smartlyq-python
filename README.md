# SmartlyQ Python SDK

[![PyPI](https://img.shields.io/pypi/v/smartlyq)](https://pypi.org/project/smartlyq/)

The official Python SDK for the [SmartlyQ API](https://docs.smartlyq.com) - social posting and scheduling, AI content generation (articles, images, video, audio, presentations), SEO research, CRM, chatbots, and more, from one API key.

- **Every endpoint covered** - the full API surface, generated from the OpenAPI spec.
- **One light dependency** - built on `httpx`.
- **Batteries included** - automatic retries with backoff, idempotency keys, request timeouts, typed errors.

## Installation

```bash
pip install smartlyq
```

## Quickstart

```python
from smartlyq import SmartlyQ

sq = SmartlyQ()  # reads SMARTLYQ_API_KEY, or pass api_key="sqk_live_..."

# Who am I?
me = sq.account.get_me()

# Generate an image with AI
image = sq.images.generate({"prompt": "A minimalist product shot of a smart speaker"})

# Publish a social post
post = sq.social.create_post({
    "text": "Hello from the SmartlyQ SDK!",
    "account_ids": ["acc_123"],
})
```

Get an API key from your [Developer Dashboard](https://app.smartlyq.com). Keys look like `sqk_live_...` (production) or `sqk_test_...` (sandbox - free simulated responses, no charges).

## Configuration

```python
sq = SmartlyQ(
    api_key="sqk_live_...",  # or set SMARTLYQ_API_KEY
    timeout=60.0,             # per-request timeout in seconds
    max_retries=2,            # automatic retries on 429/5xx
)
```

Per-request options are keyword arguments on every method:

```python
sq.social.create_post(
    body,
    idempotency_key="my-unique-key",  # safe retries for writes
    profile_id="prof_123",            # act on behalf of a managed Profile
    timeout=10.0,
)
```

## Async jobs

Generation endpoints (articles, images, videos, audio) are asynchronous: they return a job. Poll it until it completes:

```python
import time

result = sq.videos.generate({"prompt": "A 5s product teaser", "model": "standard"})
job_id = result["data"]["job_id"]

job = sq.jobs.get(job_id)
while job["data"]["status"] in ("queued", "processing"):
    time.sleep(3)
    job = sq.jobs.get(job_id)
print(job["data"]["result"])
```

## Error handling

Every non-2xx response raises `SmartlyQError`:

```python
from smartlyq import SmartlyQ, SmartlyQError

try:
    sq.articles.generate({"topic": "AI trends"})
except SmartlyQError as err:
    print(err.status_code, err.code, err, err.request_id)
```

## API Reference

All methods below are available on the client. Full request/response documentation lives at [docs.smartlyq.com](https://docs.smartlyq.com).

<!-- BEGIN GENERATED REFERENCE -->

### Account

| Method | Endpoint | Description |
| --- | --- | --- |
| `sq.account.get_me()` | `GET /me` | Get current user profile |
| `sq.account.get_me_usage(query=None)` | `GET /me/usage` | Get usage summary |
| `sq.account.get_me_balance()` | `GET /me/balance` | Get wallet balance |
| `sq.account.get_billing()` | `GET /me/billing` | Billing overview |

### AI Captain

| Method | Endpoint | Description |
| --- | --- | --- |
| `sq.captain.send_message(body)` | `POST /captain/messages` | Send AI Captain message |
| `sq.captain.list_conversations(query=None)` | `GET /captain/conversations` | List AI Captain conversations |
| `sq.captain.get_conversation(conversation_id)` | `GET /captain/conversations/{conversation_id}` | Get AI Captain conversation |

### Analytics

| Method | Endpoint | Description |
| --- | --- | --- |
| `sq.analytics.get_overview(query=None)` | `GET /analytics/overview` | Get analytics overview |
| `sq.analytics.get_posts(query=None)` | `GET /analytics/posts` | Get post analytics |
| `sq.analytics.get_account(account_id, query=None)` | `GET /analytics/accounts/{account_id}` | Get account analytics |
| `sq.analytics.daily_metrics(query=None)` | `GET /analytics/daily-metrics` | Daily metrics |
| `sq.analytics.best_time(query=None)` | `GET /analytics/best-time` | Best time to post |
| `sq.analytics.content_decay(query=None)` | `GET /analytics/content-decay` | Content decay |
| `sq.analytics.posting_frequency(query=None)` | `GET /analytics/posting-frequency` | Posting frequency vs engagement |
| `sq.analytics.post_timeline(post_id)` | `GET /analytics/posts/{post_id}/timeline` | Post metric timeline |
| `sq.analytics.inbox_volume(query=None)` | `GET /analytics/inbox/volume` | Inbox volume |
| `sq.analytics.inbox_heatmap(query=None)` | `GET /analytics/inbox/heatmap` | Inbox heatmap |
| `sq.analytics.inbox_source_breakdown(query=None)` | `GET /analytics/inbox/source-breakdown` | Inbox source breakdown |
| `sq.analytics.inbox_response_time(query=None)` | `GET /analytics/inbox/response-time` | Inbox response time |
| `sq.analytics.inbox_top_accounts(query=None)` | `GET /analytics/inbox/top-accounts` | Inbox top accounts |
| `sq.analytics.inbox_conversations(query=None)` | `GET /analytics/inbox/conversations` | Inbox conversation stats |
| `sq.analytics.inbox_conversation_detail(conversation_id)` | `GET /analytics/inbox/conversations/{conversation_id}` | Conversation analytics |

### Articles

| Method | Endpoint | Description |
| --- | --- | --- |
| `sq.articles.generate(body)` | `POST /articles/generate` | Generate article |
| `sq.articles.list(query=None)` | `GET /articles` | List articles |
| `sq.articles.get(article_id)` | `GET /articles/{article_id}` | Get article |
| `sq.articles.delete(article_id)` | `DELETE /articles/{article_id}` | Delete article |

### Audio

| Method | Endpoint | Description |
| --- | --- | --- |
| `sq.audio.text_to_speech(body)` | `POST /audio/text-to-speech` | Text to speech |
| `sq.audio.speech_to_text(body)` | `POST /audio/speech-to-text` | Speech to text |
| `sq.audio.get(audio_id)` | `GET /audio/{audio_id}` | Get audio |

### Automations

| Method | Endpoint | Description |
| --- | --- | --- |
| `sq.automations.list(query=None)` | `GET /automations` | List automations |
| `sq.automations.get(automation_id)` | `GET /automations/{automation_id}` | Get automation |
| `sq.automations.activate(automation_id)` | `POST /automations/{automation_id}/activate` | Activate automation |
| `sq.automations.deactivate(automation_id)` | `POST /automations/{automation_id}/deactivate` | Pause automation |
| `sq.automations.trigger(automation_id, body=None)` | `POST /automations/{automation_id}/trigger` | Trigger automation |
| `sq.automations.list_runs(automation_id, query=None)` | `GET /automations/{automation_id}/runs` | List runs |
| `sq.automations.get_run(automation_id, run_id)` | `GET /automations/{automation_id}/runs/{run_id}` | Get run |

### Chatbot

| Method | Endpoint | Description |
| --- | --- | --- |
| `sq.chatbots.list(query=None)` | `GET /chatbots` | List chatbots |
| `sq.chatbots.create(body)` | `POST /chatbots` | Create chatbot |
| `sq.chatbots.get(id)` | `GET /chatbots/{id}` | Get chatbot |
| `sq.chatbots.update(id, body)` | `PATCH /chatbots/{id}` | Update chatbot |
| `sq.chatbots.delete(id)` | `DELETE /chatbots/{id}` | Delete chatbot |
| `sq.chatbots.train(id)` | `POST /chatbots/{id}/train` | Start chatbot training |
| `sq.chatbots.get_train_status(id)` | `GET /chatbots/{id}/train-status` | Get chatbot training status |
| `sq.chatbots.send_message(id, body)` | `POST /chatbots/{id}/messages` | Send chatbot message |
| `sq.chatbots.list_conversations(id, query=None)` | `GET /chatbots/{id}/conversations` | List chatbot conversations |
| `sq.chatbots.get_conversation_messages(id, conv_id)` | `GET /chatbots/{id}/conversations/{conv_id}/messages` | Get conversation messages |

### Comments

| Method | Endpoint | Description |
| --- | --- | --- |
| `sq.comments.list(query=None)` | `GET /social/comments` | List comments |
| `sq.comments.reply_to(comment_id, body)` | `POST /social/comments/{comment_id}/reply` | Reply to a comment |
| `sq.comments.hide(comment_id)` | `POST /social/comments/{comment_id}/hide` | Hide or unhide a comment |
| `sq.comments.delete(comment_id)` | `DELETE /social/comments/{comment_id}` | Delete a comment |
| `sq.comments.get_post(post_id)` | `GET /social/comments/{post_id}` | Get one post's comments (threaded) |

### Content

| Method | Endpoint | Description |
| --- | --- | --- |
| `sq.content.rewrite(body)` | `POST /content/rewrite` | Rewrite content |
| `sq.content.generate_caption(body=None)` | `POST /content/caption` | Generate a social caption |

### CRM

| Method | Endpoint | Description |
| --- | --- | --- |
| `sq.crm.delete_contact(id)` | `DELETE /contacts/{id}` | Delete contact |
| `sq.crm.update_custom_field(id, body)` | `PATCH /custom-fields/{id}` | Update custom field |
| `sq.crm.bulk_import_contacts(body)` | `POST /contacts/bulk` | Bulk import contacts |
| `sq.crm.contact_channels(id)` | `GET /contacts/{id}/channels` | Contact channels |

### CRM Contacts

| Method | Endpoint | Description |
| --- | --- | --- |
| `sq.contacts.list(query=None)` | `GET /contacts` | List contacts |
| `sq.contacts.create(body)` | `POST /contacts` | Create or upsert a contact |
| `sq.contacts.get(id)` | `GET /contacts/{id}` | Get a contact |
| `sq.contacts.update(id, body)` | `PATCH /contacts/{id}` | Update a contact |
| `sq.contacts.add_tags(id, body)` | `POST /contacts/{id}/tags` | Add tags to a contact |
| `sq.contacts.remove_tags(id, body)` | `DELETE /contacts/{id}/tags` | Remove tags from a contact |
| `sq.contacts.list_notes(id)` | `GET /contacts/{id}/notes` | List contact notes |
| `sq.contacts.add_note(id, body)` | `POST /contacts/{id}/notes` | Add a note to a contact |
| `sq.contacts.enroll(id, body)` | `POST /contacts/{id}/enroll` | Enroll a contact in an automation |
| `sq.contacts.add_message(id, body)` | `POST /contacts/{id}/messages` | Log a message on a contact's timeline |
| `sq.contacts.set_field(id, slug, body)` | `PUT /contacts/{id}/fields/{slug}` | Set one custom field |
| `sq.contacts.clear_field(id, slug)` | `DELETE /contacts/{id}/fields/{slug}` | Clear one custom field |

### CRM Custom Fields

| Method | Endpoint | Description |
| --- | --- | --- |
| `sq.custom_fields.list()` | `GET /custom-fields` | List custom fields |
| `sq.custom_fields.create(body)` | `POST /custom-fields` | Create a custom field |
| `sq.custom_fields.delete(id)` | `DELETE /custom-fields/{id}` | Delete a custom field |

### CRM Opportunities

| Method | Endpoint | Description |
| --- | --- | --- |
| `sq.opportunities.list_pipelines()` | `GET /pipelines` | List pipelines |
| `sq.opportunities.create_pipeline(body)` | `POST /pipelines` | Create a pipeline |
| `sq.opportunities.list(query=None)` | `GET /opportunities` | List opportunities |
| `sq.opportunities.create(body)` | `POST /opportunities` | Create an opportunity |
| `sq.opportunities.get(id)` | `GET /opportunities/{id}` | Get an opportunity |
| `sq.opportunities.update(id, body)` | `PATCH /opportunities/{id}` | Update an opportunity |
| `sq.opportunities.delete(id)` | `DELETE /opportunities/{id}` | Delete an opportunity |
| `sq.opportunities.update_status(id, body)` | `POST /opportunities/{id}/status` | Update opportunity status |

### Direct Messages

| Method | Endpoint | Description |
| --- | --- | --- |
| `sq.messages.list_conversations(query=None)` | `GET /social/conversations` | List DM conversations |
| `sq.messages.list(conversation_id, query=None)` | `GET /social/conversations/{conversation_id}/messages` | List messages in a conversation |
| `sq.messages.send(conversation_id, body)` | `POST /social/conversations/{conversation_id}/messages` | Send a direct message |
| `sq.messages.mark_conversation_read(conversation_id)` | `POST /social/conversations/{conversation_id}/read` | Mark a conversation read |

### Images

| Method | Endpoint | Description |
| --- | --- | --- |
| `sq.images.generate(body)` | `POST /images/generate` | Generate image |
| `sq.images.list(query=None)` | `GET /images` | List images |
| `sq.images.get(image_id)` | `GET /images/{image_id}` | Get image |
| `sq.images.delete(image_id)` | `DELETE /images/{image_id}` | Delete image |

### Jobs

| Method | Endpoint | Description |
| --- | --- | --- |
| `sq.jobs.list(query=None)` | `GET /jobs` | List jobs |
| `sq.jobs.get(job_id)` | `GET /jobs/{job_id}` | Get job |
| `sq.jobs.cancel(job_id, body=None)` | `POST /jobs/{job_id}/cancel` | Cancel job |

### Media

| Method | Endpoint | Description |
| --- | --- | --- |
| `sq.media.list(query=None)` | `GET /media` | List media |
| `sq.media.get(media_id)` | `GET /media/{media_id}` | Get media |
| `sq.media.delete(media_id)` | `DELETE /media/{media_id}` | Delete media |
| `sq.media.get_upload_url(body)` | `POST /media/upload-url` | Get presigned upload URL |
| `sq.media.upload_direct(body)` | `POST /media/upload-direct` | Upload a file directly |

### Presentations

| Method | Endpoint | Description |
| --- | --- | --- |
| `sq.presentations.generate(body)` | `POST /presentations/generate` | Generate presentation |
| `sq.presentations.list(query=None)` | `GET /presentations` | List presentations |
| `sq.presentations.get(presentation_id)` | `GET /presentations/{presentation_id}` | Get presentation |
| `sq.presentations.delete(presentation_id)` | `DELETE /presentations/{presentation_id}` | Delete presentation |

### Profiles

| Method | Endpoint | Description |
| --- | --- | --- |
| `sq.profiles.list(query=None)` | `GET /profiles` | List profiles |
| `sq.profiles.create(body)` | `POST /profiles` | Create a profile |
| `sq.profiles.get(id)` | `GET /profiles/{id}` | Get a profile |
| `sq.profiles.update(id, body)` | `PATCH /profiles/{id}` | Update a profile |
| `sq.profiles.delete(id, body)` | `DELETE /profiles/{id}` | Delete a profile |
| `sq.profiles.list_accounts(id)` | `GET /profiles/{id}/accounts` | List a profile's connected accounts |
| `sq.profiles.pause(id)` | `POST /profiles/{id}/pause` | Pause a profile |
| `sq.profiles.resume(id)` | `POST /profiles/{id}/resume` | Resume a profile |
| `sq.profiles.create_connect_link(id, body=None)` | `POST /profiles/{id}/connect-link` | Create a hosted connect link |
| `sq.profiles.create_connect_url(id, platform, body=None)` | `POST /profiles/{id}/connect/{platform}` | Get a raw connect URL for one platform |
| `sq.profiles.get_account_billing()` | `GET /me/account-billing` | Account billing summary |

### Reviews

| Method | Endpoint | Description |
| --- | --- | --- |
| `sq.reviews.list(query=None)` | `GET /reviews` | List reviews |
| `sq.reviews.reply_to(review_id, body)` | `POST /reviews/{review_id}/reply` | Reply to review |
| `sq.reviews.delete_reply(review_id)` | `DELETE /reviews/{review_id}/reply` | Delete review reply |
| `sq.reviews.sync(body=None)` | `POST /reviews/sync` | Sync reviews |

### SEO

| Method | Endpoint | Description |
| --- | --- | --- |
| `sq.seo.keyword_research(body)` | `POST /seo/keyword-research` | Keyword research |
| `sq.seo.serp(body)` | `POST /seo/serp` | Live SERP lookup |
| `sq.seo.keyword_difficulty(body)` | `POST /seo/keyword-difficulty` | Keyword difficulty |
| `sq.seo.ranked_keywords(body)` | `POST /seo/ranked-keywords` | Ranked keywords (rank tracking) |
| `sq.seo.domain_overview(body)` | `POST /seo/domain-overview` | Domain rank overview |
| `sq.seo.competitors(body)` | `POST /seo/competitors` | Organic competitors |
| `sq.seo.backlinks_summary(body)` | `POST /seo/backlinks-summary` | Backlink profile summary |
| `sq.seo.audit(body)` | `POST /seo/audit` | On-page SEO audit |
| `sq.seo.backlink_prospects(body)` | `POST /seo/backlink-prospects` | Backlink prospects (link gap) |
| `sq.seo.referring_domains(body)` | `POST /seo/referring-domains` | Referring domains |
| `sq.seo.backlink_anchors(body)` | `POST /seo/backlink-anchors` | Backlink anchors |
| `sq.seo.spam_score(body)` | `POST /seo/spam-score` | Backlink spam score |
| `sq.seo.rank_history(body)` | `POST /seo/rank-history` | Historical rank overview |
| `sq.seo.site_audit(body)` | `POST /seo/site-audit` | Deep site audit |
| `sq.seo.brand_lookup(body)` | `POST /seo/brand-lookup` | AI Visibility: brand lookup |
| `sq.seo.prompt_explorer(body)` | `POST /seo/prompt-explorer` | AI Visibility: prompt explorer |
| `sq.seo.ai_audit(body)` | `POST /seo/ai-audit` | AI Visibility Audit (async) |

### Shorts

| Method | Endpoint | Description |
| --- | --- | --- |
| `sq.shorts.generate(body=None)` | `POST /shorts/generate` | Generate viral shorts from a long video |
| `sq.shorts.list(query=None)` | `GET /shorts` | List shorts jobs |
| `sq.shorts.get(uid)` | `GET /shorts/{uid}` | Get shorts job + clips |

### Social

| Method | Endpoint | Description |
| --- | --- | --- |
| `sq.social.list_accounts()` | `GET /social/accounts` | List social accounts |
| `sq.social.list_posts(query=None)` | `GET /social/posts` | List social posts |
| `sq.social.create_post(body)` | `POST /social/posts` | Create post (publish immediately) |
| `sq.social.schedule_post(body)` | `POST /social/posts/schedule` | Schedule post |
| `sq.social.get_post(post_id)` | `GET /social/posts/{post_id}` | Get social post |
| `sq.social.update_post(post_id, body)` | `PATCH /social/posts/{post_id}` | Update social post |
| `sq.social.delete_post(post_id)` | `DELETE /social/posts/{post_id}` | Delete social post |
| `sq.social.update_account(account_id, body)` | `PATCH /social/accounts/{account_id}` | Rename account |
| `sq.social.disconnect_account(account_id)` | `DELETE /social/accounts/{account_id}` | Disconnect a social account |
| `sq.social.get_account_health(account_id)` | `GET /social/accounts/{account_id}/health` | Account health |
| `sq.social.get_account_reconnect_url(account_id)` | `GET /social/accounts/{account_id}/reconnect-url` | Account reconnect URL |
| `sq.social.pause_account(account_id)` | `POST /social/accounts/{account_id}/pause` | Pause posting to an account |
| `sq.social.resume_account(account_id)` | `POST /social/accounts/{account_id}/resume` | Resume posting to an account |
| `sq.social.retry_post(post_id, body)` | `POST /social/posts/{post_id}/retry` | Retry publishing a post |
| `sq.social.connect_account_status(platform)` | `GET /social/connect/{platform}` | Poll headless connection status |
| `sq.social.connect_account(platform, body=None)` | `POST /social/connect/{platform}` | Start headless account connection |
| `sq.social.list_queues()` | `GET /social/queues` | List queues |
| `sq.social.create_queue(body)` | `POST /social/queues` | Create queue |
| `sq.social.get_queue(queue_id)` | `GET /social/queues/{queue_id}` | Get queue |
| `sq.social.update_queue(queue_id, body)` | `PUT /social/queues/{queue_id}` | Update queue |
| `sq.social.delete_queue(queue_id)` | `DELETE /social/queues/{queue_id}` | Delete queue |
| `sq.social.get_queue_next_slot(queue_id)` | `GET /social/queues/{queue_id}/next-slot` | Get next open slot |
| `sq.social.preview_queue_slots(queue_id, query=None)` | `GET /social/queues/{queue_id}/preview` | Preview upcoming slots |
| `sq.social.unpublish_post(post_id, body=None)` | `POST /social/posts/{post_id}/unpublish` | Unpublish post |
| `sq.social.validate_post(body)` | `POST /social/validate/post` | Validate post content |
| `sq.social.validate_media(body)` | `POST /social/validate/media` | Validate media URL |
| `sq.social.stop_post_recycle(post_id)` | `DELETE /social/posts/{post_id}/recycle` | Stop recycling |
| `sq.social.bulk_schedule_posts(body)` | `POST /social/posts/bulk` | Bulk schedule posts |
| `sq.social.validate_bulk_batch(body)` | `POST /social/posts/bulk/validate` | Validate a bulk batch |
| `sq.social.bulk_account_health()` | `GET /social/accounts/health` | Bulk account health |
| `sq.social.account_follower_stats(query=None)` | `GET /social/accounts/follower-stats` | Follower stats |
| `sq.social.tiktok_creator_info(account_id)` | `GET /social/accounts/{account_id}/tiktok/creator-info` | TikTok creator info |
| `sq.social.move_account(account_id, body)` | `POST /social/accounts/{account_id}/move` | Move account to profile |
| `sq.social.list_account_groups()` | `GET /social/account-groups` | List account groups |
| `sq.social.create_account_group(body)` | `POST /social/account-groups` | Create account group |
| `sq.social.get_account_group(group_id)` | `GET /social/account-groups/{group_id}` | Get account group |
| `sq.social.update_account_group(group_id, body)` | `PUT /social/account-groups/{group_id}` | Update account group |
| `sq.social.delete_account_group(group_id)` | `DELETE /social/account-groups/{group_id}` | Delete account group |
| `sq.social.get_conversation(conversation_id)` | `GET /social/conversations/{conversation_id}` | Get conversation |
| `sq.social.update_conversation(conversation_id, body)` | `PATCH /social/conversations/{conversation_id}` | Archive / reopen conversation |
| `sq.social.search_conversations(query=None)` | `GET /social/conversations/search` | Search conversations |
| `sq.social.pinterest_boards(account_id)` | `GET /social/accounts/{account_id}/pinterest/boards` | Pinterest boards |
| `sq.social.youtube_playlists(account_id)` | `GET /social/accounts/{account_id}/youtube/playlists` | YouTube playlists |
| `sq.social.instagram_publishing_limit(account_id)` | `GET /social/accounts/{account_id}/instagram/publishing-limit` | Instagram publishing limit |
| `sq.social.gmb_performance(account_id, query=None)` | `GET /social/accounts/{account_id}/gmb/performance` | Google Business performance |
| `sq.social.gmb_search_keywords(account_id, query=None)` | `GET /social/accounts/{account_id}/gmb/search-keywords` | Google Business search keywords |
| `sq.social.reddit_search(account_id, query=None)` | `GET /social/accounts/{account_id}/reddit/search` | Reddit search |
| `sq.social.reddit_feed(account_id, query=None)` | `GET /social/accounts/{account_id}/reddit/feed` | Reddit feed |
| `sq.social.reddit_subreddits(account_id)` | `GET /social/accounts/{account_id}/reddit/subreddits` | Subscribed subreddits |
| `sq.social.reddit_subreddit_rules(account_id, subreddit)` | `GET /social/accounts/{account_id}/reddit/subreddits/{subreddit}/rules` | Subreddit rules |
| `sq.social.instagram_stories(account_id)` | `GET /social/accounts/{account_id}/instagram/stories` | Instagram stories |
| `sq.social.facebook_post_reactions(account_id, query=None)` | `GET /social/accounts/{account_id}/facebook/post-reactions` | Facebook post reactions |
| `sq.social.instagram_story_insights(account_id, story_id, query=None)` | `GET /social/accounts/{account_id}/instagram/stories/{story_id}/insights` | Instagram story insights |
| `sq.social.x_retweet(account_id, body)` | `POST /social/accounts/{account_id}/x/retweets` | Retweet on X |
| `sq.social.x_unretweet(account_id, tweet_id)` | `DELETE /social/accounts/{account_id}/x/retweets/{tweet_id}` | Undo retweet |
| `sq.social.edit_published_post(post_id, body)` | `POST /social/posts/{post_id}/edit` | Edit published post |
| `sq.social.update_post_metadata(post_id, body)` | `POST /social/posts/{post_id}/update-metadata` | Update YouTube metadata |
| `sq.social.sync_external_posts(body)` | `POST /social/posts/sync-external` | Sync external posts |
| `sq.social.account_insights(account_id)` | `GET /social/accounts/{account_id}/insights` | Live account insights |
| `sq.social.gmb_locations(account_id, query=None)` | `GET /social/accounts/{account_id}/gmb/locations` | List Google locations |
| `sq.social.gmb_location(account_id, query=None)` | `GET /social/accounts/{account_id}/gmb/location` | Get business info |
| `sq.social.gmb_update_location(account_id, body)` | `PATCH /social/accounts/{account_id}/gmb/location` | Update business info |
| `sq.social.gmb_attributes(account_id)` | `GET /social/accounts/{account_id}/gmb/attributes` | Get attributes |
| `sq.social.gmb_update_attributes(account_id, body)` | `PUT /social/accounts/{account_id}/gmb/attributes` | Update attributes |
| `sq.social.gmb_attribute_metadata(account_id)` | `GET /social/accounts/{account_id}/gmb/attributes/metadata` | Available attributes |
| `sq.social.gmb_media(account_id)` | `GET /social/accounts/{account_id}/gmb/media` | List media |
| `sq.social.gmb_create_media(account_id, body)` | `POST /social/accounts/{account_id}/gmb/media` | Add photo |
| `sq.social.gmb_delete_media(account_id, body)` | `DELETE /social/accounts/{account_id}/gmb/media` | Delete media |
| `sq.social.gmb_food_menus(account_id)` | `GET /social/accounts/{account_id}/gmb/food-menus` | Get food menus |
| `sq.social.gmb_update_food_menus(account_id, body)` | `PUT /social/accounts/{account_id}/gmb/food-menus` | Update food menus |
| `sq.social.gmb_place_actions(account_id)` | `GET /social/accounts/{account_id}/gmb/place-actions` | List place-action links |
| `sq.social.gmb_create_place_action(account_id, body)` | `POST /social/accounts/{account_id}/gmb/place-actions` | Create place-action link |
| `sq.social.gmb_update_place_action(account_id, body)` | `PATCH /social/accounts/{account_id}/gmb/place-actions` | Update place-action link |
| `sq.social.gmb_delete_place_action(account_id, body)` | `DELETE /social/accounts/{account_id}/gmb/place-actions` | Delete place-action link |
| `sq.social.gmb_verifications(account_id)` | `GET /social/accounts/{account_id}/gmb/verifications` | List verifications |
| `sq.social.gmb_verification_options(account_id, body=None)` | `POST /social/accounts/{account_id}/gmb/verifications/options` | Verification options |
| `sq.social.reddit_subreddit_info(account_id, subreddit)` | `GET /social/accounts/{account_id}/reddit/subreddits/{subreddit}` | Subreddit info + eligibility |
| `sq.social.x_mentions(account_id, query=None)` | `GET /social/accounts/{account_id}/x/mentions` | X mentions |
| `sq.social.send_typing_indicator(conversation_id)` | `POST /social/conversations/{conversation_id}/typing` | Typing indicator |
| `sq.social.comment_private_reply(comment_id, body)` | `POST /social/comments/{comment_id}/private-reply` | Private reply (comment-to-DM) |
| `sq.social.get_messenger_menu(account_id)` | `GET /social/accounts/{account_id}/messenger/menu` | Get Messenger menu |
| `sq.social.set_messenger_menu(account_id, body)` | `PUT /social/accounts/{account_id}/messenger/menu` | Set Messenger menu |
| `sq.social.delete_messenger_menu(account_id)` | `DELETE /social/accounts/{account_id}/messenger/menu` | Delete Messenger menu |
| `sq.social.get_ice_breakers(account_id)` | `GET /social/accounts/{account_id}/instagram/ice-breakers` | Get ice breakers |
| `sq.social.set_ice_breakers(account_id, body)` | `PUT /social/accounts/{account_id}/instagram/ice-breakers` | Set ice breakers |
| `sq.social.delete_ice_breakers(account_id)` | `DELETE /social/accounts/{account_id}/instagram/ice-breakers` | Delete ice breakers |
| `sq.social.facebook_page_insights(account_id, query=None)` | `GET /social/accounts/{account_id}/facebook/page-insights` | Facebook page insights |
| `sq.social.instagram_audience(account_id, query=None)` | `GET /social/accounts/{account_id}/instagram/audience` | Instagram audience demographics |
| `sq.social.connect_options(account_id)` | `GET /social/accounts/{account_id}/connect-options` | Connection target options |
| `sq.social.connect_select(account_id, body)` | `POST /social/accounts/{account_id}/connect-select` | Select connection target |

### URLs

| Method | Endpoint | Description |
| --- | --- | --- |
| `sq.urls.shorten(body)` | `POST /urls/shorten` | Shorten URL |
| `sq.urls.list(query=None)` | `GET /urls` | List short URLs |
| `sq.urls.get(url_id)` | `GET /urls/{url_id}` | Get short URL |
| `sq.urls.delete(url_id)` | `DELETE /urls/{url_id}` | Delete short URL |
| `sq.urls.get_stats(url_id)` | `GET /urls/{url_id}/stats` | Get short URL stats |

### Videos

| Method | Endpoint | Description |
| --- | --- | --- |
| `sq.videos.list_models()` | `GET /videos/models` | List available video models |
| `sq.videos.generate(body)` | `POST /videos/generate` | Generate video |
| `sq.videos.list(query=None)` | `GET /videos` | List videos |
| `sq.videos.get(video_id)` | `GET /videos/{video_id}` | Get video |
| `sq.videos.delete(video_id)` | `DELETE /videos/{video_id}` | Delete video |
| `sq.videos.generate_hook(body=None)` | `POST /videos/hook` | Generate a viral hook line |
| `sq.videos.suggest_broll(body)` | `POST /videos/broll-suggest` | Suggest B-roll moments |
| `sq.videos.suggest_emphasis(body)` | `POST /videos/emphasis` | Suggest on-screen emphasis |
| `sq.videos.generate_viral_thumbnail(body)` | `POST /videos/viral-thumbnail` | Generate a viral thumbnail |

### Webhooks

| Method | Endpoint | Description |
| --- | --- | --- |
| `sq.webhooks.list()` | `GET /webhooks` | List webhooks |
| `sq.webhooks.create(body)` | `POST /webhooks` | Create webhook |
| `sq.webhooks.update(id, body)` | `PUT /webhooks/{id}` | Update webhook |
| `sq.webhooks.delete(id)` | `DELETE /webhooks/{id}` | Delete webhook |
| `sq.webhooks.list_logs(query=None)` | `GET /webhooks/logs` | List webhook delivery logs |
| `sq.webhooks.test(id)` | `POST /webhooks/{id}/test` | Send test webhook |

### WhatsApp

| Method | Endpoint | Description |
| --- | --- | --- |
| `sq.whats_app.send_whats_app_message(body)` | `POST /whatsapp/messages` | Send a WhatsApp message |
| `sq.whats_app.list_whats_app_templates(query=None)` | `GET /whatsapp/templates` | List message templates |
| `sq.whats_app.create_whats_app_template(body)` | `POST /whatsapp/templates` | Create a message template |
| `sq.whats_app.get_whats_app_business_profile(query=None)` | `GET /whatsapp/business-profile` | Get business profile |
| `sq.whats_app.update_whats_app_business_profile(body)` | `PATCH /whatsapp/business-profile` | Update business profile |
| `sq.whats_app.list_whats_app_phone_numbers(query=None)` | `GET /whatsapp/phone-numbers` | List phone numbers |

### Workspaces

| Method | Endpoint | Description |
| --- | --- | --- |
| `sq.workspaces.list()` | `GET /workspaces` | List workspaces (sub-accounts) |
| `sq.workspaces.create(body)` | `POST /workspaces` | Create a workspace (sub-account) |
| `sq.workspaces.bulk_action(body)` | `POST /workspaces/bulk` | Bulk sub-account action |
| `sq.workspaces.get(id)` | `GET /workspaces/{id}` | Get a workspace (sub-account) |
| `sq.workspaces.delete(id, body)` | `DELETE /workspaces/{id}` | Delete a workspace (sub-account) |
| `sq.workspaces.disable_saas(id, body=None)` | `POST /workspaces/{id}/disable-saas` | Disable SaaS mode for a workspace |
| `sq.workspaces.pause(id)` | `POST /workspaces/{id}/pause` | Pause (suspend) a workspace |
| `sq.workspaces.resume(id)` | `POST /workspaces/{id}/resume` | Resume a paused workspace |
| `sq.workspaces.get_subscription(id)` | `GET /workspaces/{id}/subscription` | Get a sub-account's subscription |
| `sq.workspaces.get_wallet(id)` | `GET /workspaces/{id}/wallet` | Get a sub-account's wallet balance |
| `sq.workspaces.list_saas_plans()` | `GET /saas/plans` | List SaaS plans |
| `sq.workspaces.get_saas_plan(id)` | `GET /saas/plans/{id}` | Get a SaaS plan |
<!-- END GENERATED REFERENCE -->

## Regeneration

This SDK is generated from the [SmartlyQ OpenAPI spec](https://docs.smartlyq.com). When the spec changes, CI regenerates the client, README, and tests, bumps the version, and publishes to PyPI automatically.

## License

MIT
