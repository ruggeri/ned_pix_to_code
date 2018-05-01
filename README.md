## TODO

Finished writing compiler/parser/et cetera.

Now need to write the network in Keras.

## Image Network

**Layer 1**

1. Conv2D with 32 filters, kernel size (3, 3), valid padding, relu.
2. Conv2D with 32 filters, kernel size (3, 3), valid padding, relu.
3. MaxPooling2D with pool size (2, 2).
4. 25% dropout.

**Layer 2**

Repeat, but with 64 filters.

**Layer 3**

Repeat, but with 128 filters.

**Layer 4**

1. Flatten.
2. Dense connection to 1024 units, with relu.
3. Dropout of 30%.
4. Dense connection to 1024 units again, with relu.
5. Dropout of 30%.

## Context Network

Uses 48 tokens of context.

1. LSTM with 128 units. No dropout.
2. Second LSTM with 128 units. No dropout.

## Decoder Network

Repeat the image features, and concatenate with the LSTM features.

1. LSTM with 512 units.
2. LSTM with 512 units.
3. Final output: connect to a dense layer of N units, do softmax.

## Training

Used RMSprop. Clipped gradient values at 1.0.

## Other

* Used a 256x256 image.
* Batch size of 64 with 10 epochs.

## Resources

* Resource: https://arxiv.org/pdf/1705.07962.pdf
* Resource: https://github.com/tonybeltramelli/pix2code
* Resource: https://blog.floydhub.com/turning-design-mockups-into-code-with-deep-learning/
