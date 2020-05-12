
library(ggplot2)

data <- read.csv("timings.csv")

bm <- data[data$MODE=="bm", ]
td <- data[data$MODE=="td", ]
td <- td[td$N < 100, ]

q <- ggplot(td, aes(x=N,y=GEN,color=as.factor(SP),group=as.factor(SP))) +
  geom_point() +
  geom_line() +
  labs(
    title = "Trapdoor Pemutation KeyGen",
    color = "Key Size (bits)",
    x = "Number of Keywords",
    y="Time (s)"
  ) +
  theme_bw(base_size=12) +
  theme(plot.title = element_text(hjust=0.5))

# ggsave(plot=q, "trapdoor_gen.png")

q <- ggplot(bm, aes(x=N,y=PEKS,color=as.factor(SP),group=as.factor(SP))) +
  geom_point() +
  geom_line() +
  labs(
    title = "Bilinear Map PEKS",
    color="Group Size (bits)",
    x = "Number of Keywords",
    y = "Time (s)"
  ) +
  theme_bw(base_size=12) +
  theme(plot.title = element_text(hjust=0.5))

# ggsave(plot=q, "bm_peks.png")

# Plot d(PEKS)/dN against the security parameter (bilinear)

spx = unique(bm$SP)
slopes = c()
for (sp in spx) {
  bmsp <- bm[bm$SP == sp, ]
  model <- lm(bmsp$PEKS ~ bmsp$N)
  slopes <- c(slopes, model$coefficients[2])
}
dPEKSdN <- data.frame("SP" = spx, "rate" = slopes)

# Plot KeyGen against security parameter (bilinear scheme)
q <- ggplot(dPEKSdN, aes(x=SP, y=rate)) +
  geom_point() +
  geom_line() +
  labs(
    title = "Rate of Bilinear Map PEKS",
    x = "Order of P (bits)",
    y = "Rate"
  ) +
  theme_bw(base_size=12) +
  theme(plot.title = element_text(hjust=0.5))

# Plot PEKS against security parameter (group by N) (trapdoor permutations)

# (optional) d(PEKS)/d(SP) (group by N) (trapdoor permutation)

