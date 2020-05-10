
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

ggsave(plot=q, "trapdoor_gen.png")

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

ggsave(plot=q, "bm_peks.png")
