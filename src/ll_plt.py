import pandas as pd 
import matplotlib.pyplot as plt
import seaborn as sns 
sns.set_theme()
fig, axes = plt.subplots(nrows=1, ncols=6, sharey=True, sharex=True, figsize=(15,3))
NUM_SESSIONS = 100

model_name = 'dctr'

k = 5
df = pd.read_csv('experimental_results/' + model_name + '.ll.irm.' + str(k) + '.csv')
df = df[df['weight'] != 0.0]
df = df[df['sessions'] <= NUM_SESSIONS]
sns.lineplot(x="sessions", y="loglikelihood",
             hue="weight",
             data=df, ax=axes[0])

axes[0].get_legend().remove()


k = 50
df = pd.read_csv('experimental_results/' + model_name + '.ll.irm.' + str(k) + '.csv')
df = df[df['weight'] != 0.0]
df = df[df['sessions'] <= NUM_SESSIONS]
sns.lineplot(x="sessions", y="loglikelihood",
             hue="weight",
             data=df, ax=axes[1])

axes[1].get_legend().remove()


model_name = 'dcm'

k = 5
df = pd.read_csv('experimental_results/' + model_name + '.ll.irm.' + str(k) + '.csv')
df = df[df['weight'] != 0.0]
df = df[df['sessions'] <= NUM_SESSIONS]
sns.lineplot(x="sessions", y="loglikelihood",
             hue="weight",
             data=df, ax=axes[2])

axes[2].legend(loc='upper center', bbox_to_anchor=(1.1, -0.25), fancybox=False, shadow=False, ncol=7)

k = 50
df = pd.read_csv('experimental_results/' + model_name + '.ll.irm.' + str(k) + '.csv')
df = df[df['weight'] != 0.0]
df = df[df['sessions'] <= NUM_SESSIONS]
sns.lineplot(x="sessions", y="loglikelihood",
             hue="weight",
             data=df, ax=axes[3])

axes[3].get_legend().remove()



model_name = 'sdbn'

k = 5
df = pd.read_csv('experimental_results/' + model_name + '.ll.irm.' + str(k) + '.csv')
df = df[df['weight'] != 0.0]
df = df[df['sessions'] <= NUM_SESSIONS]
sns.lineplot(x="sessions", y="loglikelihood",
             hue="weight",
             data=df, ax=axes[4])

axes[4].get_legend().remove()


k = 50
df = pd.read_csv('experimental_results/' + model_name + '.ll.irm.' + str(k) + '.csv')
df = df[df['weight'] != 0.0]
df = df[df['sessions'] <= NUM_SESSIONS]
sns.lineplot(x="sessions", y="loglikelihood",
             hue="weight",
             data=df, ax=axes[5])

axes[5].get_legend().remove()


plt.savefig('experimental_results/figures/dctr.dcm.sdbn.irm.5.50.ll.pdf', format='pdf', bbox_inches='tight')


################################################################################
#### LRM #######################################################################



import pandas as pd 
import matplotlib.pyplot as plt
import seaborn as sns 

sns.set_theme()
fig, axes = plt.subplots(nrows=1, ncols=6, sharey=True, sharex=True, figsize=(15,3))
NUM_SESSIONS = 100

model_name = 'dctr'

k = 5
df = pd.read_csv('experimental_results/' + model_name + '.ll.lrm.' + str(k) + '.csv')
df = df[df['system'] != 'LemurTF_IDF']
df = df[df['system'] != 'Baseline']
df = df[df['sessions'] <= NUM_SESSIONS]
sns.lineplot(x="sessions", y="loglikelihood",
            hue="system",
            data=df, ax=axes[0])
# plt.title(str(k) + ' queries')
plt.legend(bbox_to_anchor=(1,1), loc="upper left")
axes[0].title.set_text(model_name.upper() + '\n' + str(k) + ' queries')
axes[0].get_legend().remove()

k = 50
df = pd.read_csv('experimental_results/' + model_name + '.ll.lrm.' + str(k) + '.csv')
df = df[df['system'] != 'LemurTF_IDF']
df = df[df['system'] != 'Baseline']
df = df[df['sessions'] <= NUM_SESSIONS]
sns.lineplot(x="sessions", y="loglikelihood",
            hue="system",
            data=df, ax=axes[1])
# plt.title(str(k) + ' queries')
plt.legend(bbox_to_anchor=(1,1), loc="upper left")
axes[1].title.set_text(model_name.upper() + '\n' + str(k) + ' queries')
axes[1].get_legend().remove()


model_name = 'dcm'

k = 5
df = pd.read_csv('experimental_results/' + model_name + '.ll.lrm.' + str(k) + '.csv')
df = df[df['system'] != 'LemurTF_IDF']
df = df[df['system'] != 'Baseline']
df = df.replace('XSqrA_M', 'DFR $\chi^2$')
df = df[df['sessions'] <= NUM_SESSIONS]
sns.lineplot(x="sessions", y="loglikelihood",
            hue="system",
            data=df, ax=axes[2])
# plt.title(str(k) + ' queries')
plt.legend(bbox_to_anchor=(1,1), loc="upper left")
axes[2].title.set_text(model_name.upper() + '\n' + str(k) + ' queries')
# axes[2].get_legend().remove()
# axes[2].legend(loc='upper center', bbox_to_anchor=(1.1, -0.25), fancybox=False, shadow=False, ncol=6)
axes[2].legend(loc='upper center', bbox_to_anchor=(1.1, -0.25), fancybox=False, shadow=False, ncol=6)

k = 50
df = pd.read_csv('experimental_results/' + model_name + '.ll.lrm.' + str(k) + '.csv')
df = df[df['system'] != 'LemurTF_IDF']
df = df[df['system'] != 'Baseline']
df = df[df['sessions'] <= NUM_SESSIONS]
sns.lineplot(x="sessions", y="loglikelihood",
            hue="system",
            data=df, ax=axes[3])
# plt.title(str(k) + ' queries')
plt.legend(bbox_to_anchor=(1,1), loc="upper left")
axes[3].title.set_text(model_name.upper() + '\n' + str(k) + ' queries')
axes[3].get_legend().remove()




model_name = 'sdbn'

k = 5
df = pd.read_csv('experimental_results/' + model_name + '.ll.lrm.' + str(k) + '.csv')
df = df[df['system'] != 'LemurTF_IDF']
df = df[df['system'] != 'Baseline']
df = df[df['sessions'] <= NUM_SESSIONS]
sns.lineplot(x="sessions", y="loglikelihood",
            hue="system",
            data=df, ax=axes[4])
# plt.title(str(k) + ' queries')
plt.legend(bbox_to_anchor=(1,1), loc="upper left")
axes[4].title.set_text(model_name.upper() + '\n' + str(k) + ' queries')
axes[4].get_legend().remove()

k = 50
df = pd.read_csv('experimental_results/' + model_name + '.ll.lrm.' + str(k) + '.csv')
df = df[df['system'] != 'LemurTF_IDF']
df = df[df['system'] != 'Baseline']
df = df[df['sessions'] <= NUM_SESSIONS]
sns.lineplot(x="sessions", y="loglikelihood",
            hue="system",
            data=df, ax=axes[5])
# plt.title(str(k) + ' queries')
plt.legend(bbox_to_anchor=(1,1), loc="upper left")
axes[5].title.set_text(model_name.upper() + '\n' + str(k) + ' queries')
axes[5].get_legend().remove()



plt.savefig('experimental_results/figures/dctr.dcm.sdbn.lrm.5.50.ll.pdf', format='pdf', bbox_inches='tight')
