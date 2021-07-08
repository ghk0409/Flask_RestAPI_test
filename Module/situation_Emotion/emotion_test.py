from recommand_emotion import emotion_module


em = emotion_module(395, 1)
ch_idx = em.emotion_channel_idx()
comment_idx = em.emotion_comment_idx()

print(ch_idx)
print(comment_idx)