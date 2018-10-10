# to run this test, execute the command "python3 -m unittest -v <this file>"
import leaf, pprint, unittest

class TestBTree( unittest.TestCase ):
  node = None

  def test_02_insert( self ):
    TestBTree.node = leaf.Leaf( [] )
    for n in [ 8, 5, 1, 7, 3 ]:
      TestBTree.node = TestBTree.node.insert( n )
    all = TestBTree.node.get( )
    assert all == [ 1, 3, 5, 7, 8 ] and TestBTree.node.depth( ) == 2

  def test_03_delete_middle( self ):
    TestBTree.node = TestBTree.node.delete( 5 )
    print(TestBTree.node.get())
    assert TestBTree.node.get( ) == [ 1, 3, 7, 8 ]
    TestBTree.node = TestBTree.node.insert( 5 )

  def test_04_rebalance_left( self ):
    TestBTree.node = TestBTree.node.delete( 8 )
    TestBTree.node.check( )
    assert TestBTree.node.get( ) == [ 1, 3, 5, 7 ]
    TestBTree.node = TestBTree.node.insert( 8 )

  def test_05_rebalance_right( self ):
    TestBTree.node = TestBTree.node.delete( 1 )
    TestBTree.node.check( )
    assert TestBTree.node.get( ) == [ 3, 5, 7, 8 ]
    TestBTree.node = TestBTree.node.insert( 1 )

  def test_06_lose_a_level( self ):
    for n in [ 8, 5 ]:
      TestBTree.node = TestBTree.node.delete( n )
    TestBTree.node.check( )
    assert TestBTree.node.get( ) == [ 1, 3, 7 ]
    assert isinstance( TestBTree.node, leaf.Leaf )

  def test_07_empty_tree( self ):
    for n in [ 1, 3, 7 ]:
      TestBTree.node = TestBTree.node.delete( n )
    assert TestBTree.node.get( ) == [ ]

  def test_08_three_level( self ):
    # start a new three level tree
    seq = [ 8, 5, 1, 7, 3, 12, 2, 10, 4, 9, 6, 11 ]
    TestBTree.node = leaf.Leaf( [] )
    for n in seq:
      TestBTree.node = TestBTree.node.insert( n )
    seq.sort( )
    assert seq == TestBTree.node.get( ) and TestBTree.node.depth( ) == 3

  def test_09_delete_merge( self ):
    print('\n\n')
    TestBTree.node.walk()
    seq = TestBTree.node.get( )
    TestBTree.node = TestBTree.node.delete( 10 )
    TestBTree.node.check( )
    seq.remove( 10 )
    print('\n\n')
    TestBTree.node.walk()
    assert seq == TestBTree.node.get( ) and TestBTree.node.depth( ) == 3

  def test_10_delete_shift( self ):
    seq = TestBTree.node.get( )
    TestBTree.node = TestBTree.node.delete( 1 )
    TestBTree.node.check( )
    seq.remove( 1 )
    print('\n\n')
    print(TestBTree.node.walk())
    assert seq == TestBTree.node.get( ) and TestBTree.node.depth( ) == 2
