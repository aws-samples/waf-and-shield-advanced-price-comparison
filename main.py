import numpy as np
import matplotlib.pyplot as plt

# Constants for pricing
AOS = 10  # Average Object Size (KB)
WEBACL_NUM = 1
RULE_NUM = 10
REQ_PRICE = 0.6    # 1500 WCU or less. https://aws.amazon.com/waf/pricing/
SUBSC = 3000

# Shield pricing tiers
TIER1_LIMIT = 100 * 1024
TIER2_LIMIT = 500 * 1024
TIER3_LIMIT = 1000 * 1024

# Pricing for Amazon CloudFront. Refer to https://aws.amazon.com/shield/pricing/
TIER1_PRICE = 0.025
TIER2_PRICE = 0.02
TIER3_PRICE = 0.015
TIER4_PRICE = 0.01

# Monthly request number (Million)
req = np.arange(0, 20000, 1)

# Calculate WAF monthly fee
waf = WEBACL_NUM * 5 + RULE_NUM * 1 + req * REQ_PRICE

# Calculate Shield monthly data transfer out (DTO) in GB
shield_dto = AOS * req * 1000 * 1000 / 1024 / 1024

# Calculate Shield monthly fee based on the tiers
shield = np.where(
    shield_dto <= TIER1_LIMIT,
    SUBSC + TIER1_PRICE * shield_dto,
    np.where(
        shield_dto <= TIER2_LIMIT,
        SUBSC + TIER1_PRICE * TIER1_LIMIT + TIER2_PRICE * (shield_dto - TIER1_LIMIT),
        np.where(
            shield_dto <= TIER3_LIMIT,
            SUBSC + TIER1_PRICE * TIER1_LIMIT + TIER2_PRICE * (TIER2_LIMIT - TIER1_LIMIT) + TIER3_PRICE * (shield_dto - TIER2_LIMIT),
            SUBSC + TIER1_PRICE * TIER1_LIMIT + TIER2_PRICE * (TIER2_LIMIT - TIER1_LIMIT) + TIER3_PRICE * (TIER3_LIMIT - TIER2_LIMIT) + TIER4_PRICE * (shield_dto - TIER3_LIMIT)
        )
    )
)

# Plotting the costs
plt.plot(req, waf, 'r', label='WAF Cost')        # Red line represents WAF cost
plt.plot(req, shield, 'b', label='Shield Adv Cost')  # Blue line represents Shield Adv cost
plt.title('WAF & Shield price comparison')
plt.xlabel('Requests (Million)')
plt.ylabel('Monthly cost ($)')
plt.legend()
plt.grid(True)

# Adding annotations for the lines
plt.annotate('WAF Cost', xy=(req[-1], waf[-1]), xytext=(req[-1], waf[-1] + 1000),
             fontsize=10, color='red')
plt.annotate('Shield Adv Cost', xy=(req[-1], shield[-1]), xytext=(req[-1], shield[-1] - 3000),
             fontsize=10, color='blue')

# Adding annotation for AOS
plt.annotate(f'AOS={AOS} KB', xy=(0.7 * req[-1], 0.5 * max(waf.max(), shield.max())),
             fontsize=12, bbox=dict(facecolor='white', alpha=0.5))

plt.show()