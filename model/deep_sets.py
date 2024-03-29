import tensorflow as tf
from set_utils import row_wise_mlp
from set_model import SetModel

class DeepSets(SetModel):
    def __init__(self, inputs):
        self.inputs = inputs

    def _get_model(self):
        with tf.variable_scope('deepsets'):
            # Set permequi
            tens = self.inputs
            tens = forward(tens)
            tens = forward(tens, layer=2)
            tens = forward(tens, layer=3)
            set_feats = tf.reduce_max(tens, axis=1)
            return final_pass(set_feats)

def forward(inputs, norm=tf.reduce_max, out_dim=256, layer=1):
    with tf.variable_scope('permequiv{}'.format(layer)):
        norm_val = norm(inputs, 1, keepdims=True)
        normed = inputs - norm_val
        return row_wise_mlp(normed, hidden_sizes=[out_dim], sigma=tf.nn.tanh)

def final_pass(inputs):
    return inputs
    inputs = tf.nn.dropout(inputs, rate=0.5)
    inputs = row_wise_mlp(inputs, hidden_sizes=[40], sigma=tf.nn.tanh)
    inputs = tf.nn.dropout(inputs, rate=0.5)
    return row_wise_mlp(inputs, [{'nodes': 40, 'sigma': identity}], mat=True, name="final")


if __name__ == '__main__':
    a = tf.constant([
        [[1, 2, 3], [4, 5, 6], [12, 65, 78], [0, 65, 78]], 
        [[7, 8, 9], [3, 1, 7], [12, 65, 78], [12, 1003, 78]],
    ], dtype=tf.float32)

    final = forward(forward(forward(a, out_dim=6), out_dim=6, layer=2), out_dim=6, layer=3)
    with tf.Session() as sess:
        sess.run(tf.global_variables_initializer())
        print(sess.run(final))
