# System Design Challenge

Tasked with creating a YouTube clone under the following constraints:

- 5 devs to build and maintain this product
- Public release in 6 months
- Average DAU of 20k-50k
- Users concentrated in Canada and Europe (assume 50% split)

With these guidelines in mind, I’ve extended the assumptions to better define the technical solution

- Each user watches 5 videos per day
- Average video length is 15mins
- Traffic peaks during day reach 50% of DAU
- 0.5% of users upload a video every day of an average length (15 min)
- We use Google’s recommended encoding params and a very efficient codec (VP9), and assume that the average video is watched in 1080p@30fps, at an average bitrate of 1800kbps (0.225 MB/s) ([source](https://developers.google.com/media/vp9/settings/vod))

### Conclusions:

- 1,500,000 - 3,750,000 mins of video delivered per day
- 10k-25k active connections during peak hours
- Peak bandwidth at assumed average bitrate: 2.25 GB/s - 5.625 GB/s
- 1,500 - 3,750 mins of video uploaded per day
- Daily data transfer: 20 TB - 50 TB
- Monthly data transfer: 607.5 TB - 1,518.75 TB

### What product features are important for this site?

- Video uploads by end users
    - Public and private videos
- Video interaction features
    - Likes, comments, sharing
- Channel view
    - View of liked, favourited videos
    - View of user comments

### What product experience is important?

- Low latency
- Fast uploads
- Live video interaction (comments, likes)

### How do we deliver the product experience?

- Distributed video hosting (CDN)
- Support for poor internet connections (adaptive bitrate streaming)
    - A number of ABS protocols, some proprietary
        - Dynamic Adaptive Streaming over HTTP, developed by MPEG (DASH)
        - HTTP Live Streaming, developed by Apple (HLS)
        - HTTP Dynamic Stream, developed by Adobe (HDS)
- Streaming updates about video metadata (likes, comments, etc)

## **Frontend**

I would build an SPA built in React using a modern framework like Next.js. 

Modelling this as an SPA as we build out the first iteration allows us to deliver the app quickly to end users and have the app running locally on the machines of our users. Next.js is an extensible framework that allows us to adopt more complex deployment and application patterns as our needs evolve. 

## Backend

In this section I will compare two general approaches to developing a backend for this application. The first, a homegrown solution, would be designed, developed, and maintained entirely by the main dev team. The second option will explore leveraging a third part product for hosting and for their content delivery network (CDN). In this case we will explore Cloudflare’s Stream product and AWS’ CloudFront.

In either of these cases, it would make sense to maintain a secondary service database that holds metadata about videos to isolate it from the main infrastructure that accepts and delivers video content. This is a good idea because the two parts have very different responsibilities. This service database must hold relational information about videos, users, and their interactions, whereas the CDN is focused on storing and delivering content as efficiently and quickly as possible. Having this separated architecture also allows us to complete an beta version of the product using a third party CDN but allows us the flexibility to migrate to other solutions down the line as we optimize the service. This architecture is illustrated in the following two diagrams, representing critical requests:

**Get a video to watch:**

![Screenshot_2025-03-17_at_16 50 57](https://github.com/user-attachments/assets/abeae0a7-32c7-4ae3-9fae-610fc5357178)


**Upload a video:**

![Screenshot_2025-03-17_at_16 50 21](https://github.com/user-attachments/assets/80bca1ad-95fa-48b4-8415-874de3d53575)


### DIY CDN

This would be a very complex undertaking essentially building a full CDN from scratch. This would require complex anycast DNS routing, multi-region database deploys with content being propagated out to delivery nodes as we process uploads. Given the volume of content uploaded daily (between 20-50 GB) and the content consumed daily (20-50 TB) we would need a very performant storage solution. For this reason, I haven’t explore this option in significant depth. I suspect that we would start with a third party service for CDN and slowly migrate to a cheaper, self-designed system as we learned more about how the service was being used and the hard product requirements.

### Cloudflare Stream

Cloudflare uses a unique billing model that charges for video minutes, not for the raw storage or bandwidth used to store or deliver video. Publicly available pricing is designed for small scale services with base plan limits of 10,000 mins of video stored and 50,000 mins of video delivered for $50/month. Additional video stored is at $5/1000mins and additional video delivery is at $1/1000mins.

I reached out to Cloudflare to inquire about pricing info for 100,000,000 mins of video viewed per month and 100,000 minutes of video uploaded per month but did not hear back from the sales team.

Volume discounts would surely apply as this fictional usage would be ~$100,000/month just for viewing.

### AWS CloudFront

The following is a quote for Cloudfront pricing using our assumptions from above. This includes data transfer and API requests with CDN node deployments in Canada and Europe with traffic split evenly between the two locations.

This quote does not include other infra that would be necessary like the raw content storage in S3.

<img width="1683" alt="Screenshot_2025-03-13_at_17 33 57" src="https://github.com/user-attachments/assets/b51fc6e6-89b0-4a45-90be-b73f2d278205" />

<img width="1681" alt="Screenshot_2025-03-13_at_17 35 22" src="https://github.com/user-attachments/assets/3017d432-963a-459c-ae11-3a9245036649" />
