import { describe, it, beforeEach, afterEach } from 'mocha'
import { expect }                              from 'chai'
import startApp                                from '../helpers/start-app'
import destroyApp                              from '../helpers/destroy-app'
import { authenticateSession }                 from 'timed/tests/helpers/ember-simple-auth'
import testSelector                            from 'ember-test-selectors'

describe('Acceptance | auth', function() {
  let application

  beforeEach(function() {
    application = startApp()
  })

  afterEach(function() {
    destroyApp(application)
  })

  it('prevents unauthenticated access', async function() {
    await visit('/')

    expect(currentURL()).to.equal('/login')
  })

  it('can login', async function() {
    server.create('user', { firstName: 'John', lastName: 'Doe', password: '123qwe' })

    await visit('/login')

    await fillIn('input[type=text]', 'johnd')
    await fillIn('input[type=password]', '123qwe')

    await click('button[type=submit]')

    expect(currentURL()).to.equal('/')
  })

  it('validates login', async function() {
    server.create('user', { firstName: 'John', lastName: 'Doe', password: '123qwe' })

    await visit('/login')

    await fillIn('input[type=text]', 'johnd')
    await fillIn('input[type=password]', '123123')

    await click('button[type=submit]')

    expect(currentURL()).to.equal('/login')

    await fillIn('input[type=text]', '')
    await fillIn('input[type=password]', '')

    await click('button[type=submit]')

    expect(currentURL()).to.equal('/login')
  })

  it('can logout', async function() {
    await authenticateSession(application)

    await visit('/')

    expect(currentURL()).to.equal('/')

    await click(testSelector('logout'))

    expect(currentURL()).to.equal('/login')
  })
})