@isTest
private class HelloWorldTest {
    @isTest
    static void testHello() {
        String result = HelloWorld.sayHello();
        System.assertEquals('Hello DevOps POC!', result, 'Validate message');
    }
}