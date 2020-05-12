
library(ggplot2)
library(reshape2)
library(plyr)
library(boot)
library(simpleboot)

# datFull <- read.csv("timings.csv")
datFull <- read.csv("timings/timings--2020-05-11--23-19-33.csv")

data <- ddply(datFull, c("MODE", "N", "SP"), summarise,
              GENmin = boot.ci(one.boot(GEN, mean, R=100), type="basic")$basic[4],
              GENmax = boot.ci(one.boot(GEN, mean, R=100), type="basic")$basic[5],
              GEN = mean(GEN),
              PEKSmin = boot.ci(one.boot(PEKS, mean, R=100), type="basic")$basic[4],
              PEKSmax = boot.ci(one.boot(PEKS, mean, R=100), type="basic")$basic[5],
              PEKS = mean(PEKS),
              TRAPDOORmin = boot.ci(one.boot(TRAPDOOR, mean, R=100), type="basic")$basic[4],
              TRAPDOORmax = boot.ci(one.boot(TRAPDOOR, mean, R=100), type="basic")$basic[5],
              TRAPDOOR = mean(TRAPDOOR),
              TESTmin = boot.ci(one.boot(TEST, mean, R=100), type="basic")$basic[4],
              TESTmax = boot.ci(one.boot(TEST, mean, R=100), type="basic")$basic[5],
              TEST = mean(TEST)
        )

bm <- data[data$MODE=="bm", ]
td <- data[data$MODE=="td", ]

q <- ggplot(td, aes(x=N,y=GEN,color=as.factor(SP),group=as.factor(SP))) +
  geom_point() +
  geom_line() +
  geom_errorbar(aes(ymin=GENmin,ymax=GENmax)) +
  labs(
    title = "Trapdoor Pemutation KeyGen",
    color = "Key Size (bits)",
    x = "Number of Keywords",
    y="Time (s)"
  ) +
  theme_bw(base_size=12) +
  theme(plot.title = element_text(hjust=0.5))

ggsave(plot=q, "td_gen.png")

q <- ggplot(bm, aes(x=N,y=GEN,color=as.factor(SP),group=as.factor(SP))) +
  geom_point() +
  geom_line() +
  geom_errorbar(aes(ymin=GENmin,ymax=GENmax)) +
  labs(
    title = "Blinear Map KeyGen",
    color = "Key Size (bits)",
    x = "Number of Keywords",
    y="Time (s)"
  ) +
  theme_bw(base_size=12) +
  theme(plot.title = element_text(hjust=0.5))

ggsave(plot=q, "bm_gen.png")

q <- ggplot(td, aes(x=N,y=log(GEN,base=2),color=as.factor(SP),group=as.factor(SP))) +
  geom_point() +
  geom_line() +
  geom_errorbar(aes(ymin=log(GENmin,base=2),ymax=log(GENmax,base=2))) +
  labs(
    title = "Trapdoor Pemutation KeyGen (log scale)",
    color = "Key Size (bits)",
    x = "Number of Keywords",
    y="Log of Time"
  ) +
  theme_bw(base_size=12) +
  theme(plot.title = element_text(hjust=0.5))

ggsave(plot=q, "td_gen_log.png")

q <- ggplot(bm, aes(x=N,y=PEKS,color=as.factor(SP),group=as.factor(SP))) +
  geom_point() +
  geom_line() +
  geom_errorbar(aes(ymin=PEKSmin,ymax=PEKSmax)) +
  labs(
    title = "Bilinear Map PEKS",
    color="Group Size (bits)",
    x = "Number of Keywords",
    y = "Time (s)"
  ) +
  theme_bw(base_size=12) +
  theme(plot.title = element_text(hjust=0.5))

ggsave(plot=q, "bm_peks.png")

# Plot d(PEKS)/dN against the security parameter (bilinear)

rates <- ddply(data, c("MODE", "SP"), summarise,
               dGENdN = lm(GEN ~ N)$coefficients[2],
               dPEKdN = lm(PEKS ~ N)$coefficients[2],
               dTRAPdN = lm(TRAPDOOR ~ N)$coefficients[2],
               dTESTdN = lm(TEST ~ N)$coefficients[2]
        )

q <- ggplot(rates[rates$MODE=="bm",], aes(x=SP, y=dPEKdN)) +
  geom_point() +
  geom_line() +
  labs(
    title = "Bilinear Map PEKS Rates",
    x = "Group Size (bits)",
    y = "Rate (s/kw)"
  ) +
  theme_bw(base_size=12) +
  theme(plot.title = element_text(hjust=0.5))

ggsave(plot=q, "bm_dpeks_dn.png")

q <- ggplot(rates[rates$MODE=="td",], aes(x=SP, y=dPEKdN)) +
  geom_point() +
  geom_line() +
  labs(
    title = "Trapdoor Permutation PEKS Rates",
    x = "Key Size (bits)",
    y = "Rate (s/kw)"
  ) +
  theme_bw(base_size=12) +
  theme(plot.title = element_text(hjust=0.5))

ggsave(plot=q, "td_dpeks_dn.png")

# Plot PEKS against security parameter (group by N) (trapdoor permutations)

q <- ggplot(td, aes(x=N,y=PEKS,color=as.factor(SP),group=as.factor(SP))) +
  geom_point() +
  geom_line() +
  geom_errorbar(aes(ymin=PEKSmin,ymax=PEKSmax)) +
  labs(
    title = "Trapdoor Permutation PEKS",
    color="Group Size (bits)",
    x = "Number of Keywords",
    y = "Time (s)"
  ) +
  theme_bw(base_size=12) +
  theme(plot.title = element_text(hjust=0.5))

ggsave(plot=q, "td_peks.png")

labels <- c(`bm` = "Bilinear Map", `td` = "Trapdoor Permutation")

q <- ggplot(data, aes(x=N,y=PEKS,color=as.factor(SP),group=as.factor(SP))) +
  geom_point() +
  geom_line() +
  geom_errorbar(aes(ymin=PEKSmin,ymax=PEKSmax)) +
  facet_grid(~ MODE, labeller=as_labeller(labels)) +
  labs(
    title = "PEKS",
    color="Key Size (bits)",
    x = "Number of Keywords",
    y = "Time (s)"
  ) +
  theme_bw(base_size=12) +
  theme(plot.title = element_text(hjust=0.5))

ggsave(plot=q, "all_peks.png", width=10)

q <- ggplot(data, aes(x=N,y=TEST,color=as.factor(SP),group=as.factor(SP))) +
  geom_point() +
  geom_line() +
  geom_errorbar(aes(ymin=TESTmin,ymax=TESTmax)) +
  facet_grid(~ MODE, labeller=as_labeller(labels)) +
  labs(
    title = "TEST",
    color="Key Size (bits)",
    x = "Number of Keywords",
    y = "Time (s)"
  ) +
  theme_bw(base_size=12) +
  theme(plot.title = element_text(hjust=0.5))

ggsave(plot=q, "all_test.png", width=10)
