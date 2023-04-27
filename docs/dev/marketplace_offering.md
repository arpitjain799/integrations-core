---
title: Build A Marketplace Offering
type: documentation
aliases: 
- 'developers/marketplace/'
dependencies: "https://github.com/DataDog/integrations-core/blob/alai97/add-marketplace-documentation/docs/dev/marketplace_offering.md"
further_reading:
- link: "https://www.datadoghq.com/partner/"
  tag: "Partner Network"
  text: "Datadog Partner Network"
- link: "https://www.datadoghq.com/blog/datadog-marketplace/"
  tag: "Blog"
  text: "Expand your monitoring reach with the Datadog Marketplace"
- link: "/developers/integrations/marketplace_offering/"
  tag: "Documentation"
  text: "Learn how to develop a Marketplace offering"
- link: "/developers/datadog_apps/"
  tag: "Documentation"
  text: "Learn about Datadog Apps"
---

## Overview

The Datadog Marketplace is a digital marketplace where Datadog Technology Partners can list their paid offerings to Datadog users.  

While the **Integrations** page includes integrations built by both Datadog and Technology Partners at no cost, the **Marketplace**  is a commercial platform for Datadog customers and Technology Partners to buy and sell a variety of offerings including Agent-based or API-based integrations, software licenses, and professional services.

## List an offering 

All Technology Partners can list an out-of-the-box integration on the **Integrations** page, or a commercial paid offering on the **Marketplace** page. The following types of offerings are supported on the Datadog Marketplace:

### Integrations
Marketplace integrations that submit third-party data or pull data from a user's Datadog account through the [Datadog Agent][15] or the [Datadog API][16]. These integrations can contain a variety of data types, such as metrics, events, logs, traces, and more.

### Software licenses
Software licenses enable you to deliver and license software solutions to customers through the Datadog Marketplace.

### Professional services
[Professional services][18] enable you to offer your team's services for implementation, support, or management for a set period of time.

## Why join the Datadog Marketplace? 

Marketplace Partners have unique benefits that are not available to partners who list out-of-the-box integrations:
 
  - Go-to-Market collaboration, including a blog post, a quote for a press release, and social media amplification, with access to dedicated sales and marketing resources focused on accelerating partner growth. 

  - Training and Support for sales enablement in the form of on-demand courses to quickly onboard sales and technical teams.

  - Exclusive opportunities to sponsor conferences and events (such as Datadog DASH) at a discounted rate.
  
  - Generating new leads from user discovery

{{< img src="developers/marketplace/marketplace_overview.png" alt="The Datadog Marketplace page" style="width:100%" >}}

## Join the Datadog partner network

Before listing an offering on the Datadog Marketplace, you will first need to apply to the [Datadog Partner Network's][3] **Technology Partner** track. Once your application has been approved, you can begin to develop your offering.

## Request a sandbox account

All Technology Partners can request a dedicated sandbox Datadog account to aid in their development.

To request a sandbox account:

1. Log into the [Datadog Partner Portal][6].
2. On your personal homepage, click on the **Learn More** button under **Sandbox Access**.
3. Select **Request Sandbox Upgrade**.

<div class="alert alert-info">If you are already a member of a Datadog organization (including a trial org), you may need to switch to your newly created sandbox. For more information, see the <a href="https://docs.datadoghq.com/account_management/org_switching/">Account Management documentation</a>.</div>

Creating a developer sandbox may take up to one or two business days. Once your sandbox is created, you can [invite new members from your organization][7] to collaborate with.

## Explore learning resources

Once you've joined the Technology Partner track and requested a sandbox account, you can start learning about developing offerings by:

* Completing the on-demand [**Introduction to Datadog Integrations**][8] course on the [Datadog Learning Center][9].
* Reading the documentation about setting up an [OAuth 2.0 client][11] for API-based integrations.


### Request access to Marketplace

To request access to the private Marketplace repository, email <a href="mailto:marketplace@datadoghq.com">marketplace@datadoghq.com</a>. Once you have been granted access, you can review an [example pull request][12] in the Marketplace repository with annotations and best practices.

## Coordinate GTM opportunities

Once a Marketplace tile is live, Technology Partners can meet with Datadog's Partner Marketing team to coordinate a joint go-to-market (GTM) strategy, which includes the following:

- A Datadog quote for partner press releases
- A blog post on the [Datadog Monitor][23]
- Amplification of social media posts

## Getting Started
To get started with creating an offering, see [Create a Tile][13]. If you're interesting in building an Agent-based integration and selling it on the Datadog Marketplace, see [Create an Agent-based Integration][19].

## Further Reading

{{< partial name="whats-next/whats-next.html" >}}

[1]: https://app.datadoghq.com/integrations
[2]: https://app.datadoghq.com/marketplace
[3]: https://partners.datadoghq.com/
[4]: https://docs.datadoghq.com/developers/integrations/new_check_howto/
[5]: https://docs.datadoghq.com/developers/datadog_apps
[6]: https://partners.datadoghq.com/English/
[7]: /account_management/users/#add-new-members-and-manage-invites
[8]: https://learn.datadoghq.com/courses/intro-to-integrations
[9]: https://learn.datadoghq.com/
[10]: https://chat.datadoghq.com/
[11]: https://docs.datadoghq.com/developers/authorization/
[12]: https://github.com/DataDog/marketplace/pull/107
[13]: https://docs.datadoghq.com/developers/integrations/create_a_tile
[14]: https://docs.datadoghq.com/developers/integrations/api_integration/
[15]: https://docs.datadoghq.com/integrations/create_a_tile/#agent-based-integrations
[16]: https://docs.datadoghq.com/integrations/create_a_tile/#rest-api-integrations
[17]: https://docs.datadoghq.com/integrations/create_a_tile/#datadog-apps
[18]: https://docs.datadoghq.com/integrations/create_a_tile/#saas-license-or-professional-service-offerings
[19]: https://docs.datadoghq.com/developers/integrations/agent_integration